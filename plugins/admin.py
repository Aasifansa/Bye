import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *



# Commands for adding admins by owner
@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    check = 0
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>You need to provide user ID(s) to add as admin.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/add_admin [user_id]</code> — Add one or more user IDs\n\n"
            "<b>Example:</b>\n"
            "<code>/add_admin 1234567890 9876543210</code>",
            reply_markup=reply_markup
        )

    admin_list = ""
    for id in admins:
        try:
            id = int(id)
        except:
            admin_list += f"<blockquote><b>Invalid ID: <code>{id}</code></b></blockquote>\n"
            continue

        if id in admin_ids:
            admin_list += f"<blockquote><b>ID <code>{id}</code> already exists.</b></blockquote>\n"
            continue

        id = str(id)
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(ID: <code>{id}</code>) added.</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>Invalid ID: <code>{id}</code></b></blockquote>\n"

    if check == len(admins):
        for id in admins:
            await db.add_admin(int(id))
        await pro.edit(f"<b>✅ Admin(s) added successfully:</b>\n\n{admin_list}", reply_markup=reply_markup)
    else:
        await pro.edit(
            f"<b>❌ Some errors occurred while adding admins:</b>\n\n{admin_list.strip()}\n\n"
            "<b><i>Please check and try again.</i></b>",
            reply_markup=reply_markup
        )


@Bot.on_message(filters.command('deladmin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>Please provide valid admin ID(s) to remove.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/deladmin [user_id]</code> — Remove specific IDs\n"
            "<code>/deladmin all</code> — Remove all admins",
            reply_markup=reply_markup
        )

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await db.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔️ All admin IDs have been removed:</b>\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>No admin IDs to remove.</blockquote></b>", reply_markup=reply_markup)

    if admin_ids:
        passed = ''
        for admin_id in admins:
            try:
                id = int(admin_id)
            except:
                passed += f"<blockquote><b>Invalid ID: <code>{admin_id}</code></b></blockquote>\n"
                continue

            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅ Removed</blockquote>\n"
            else:
                passed += f"<blockquote><b>ID <code>{id}</code> not found in admin list.</b></blockquote>\n"

        await pro.edit(f"<b>⛔️ Admin removal result:</b>\n\n{passed}", reply_markup=reply_markup)
    else:
        await pro.edit("<b><blockquote>No admin IDs available to delete.</blockquote></b>", reply_markup=reply_markup)


@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ No admins found.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await pro.edit(f"<b>⚡ Current Admin List:</b>\n\n{admin_list}", reply_markup=reply_markup)


# --- Premium User Management Commands ---

@Bot.on_message(filters.command('add') & filters.private & admin)
async def add_premium_user(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not args:
        return await pro.edit(
            "<b>Please provide a user ID to add to Premium.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/add [user_id]</code>",
            reply_markup=reply_markup
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ Invalid User ID! Please provide a numeric user ID.</b>", reply_markup=reply_markup)

    try:
        # Database mein premium add karne ka function call
        if hasattr(db, 'add_premium'):
            await db.add_premium(user_id)
        
        # Target user ki details fetch karne ki koshish
        try:
            target_user = await client.get_users(user_id)
        except:
            target_user = message.from_user

        # --- Premium Verification Log Details ---
        joined_date = datetime.now().strftime("%d-%b-%Y")
        expire_date = (datetime.now() + timedelta(days=30)).strftime("%d-%b-%Y") # Default 30 Days expiry

        premium_log_text = (
            f"<b>⚡ #PREMIUM_USER_ADDED</b>\n\n"
            f"<b>👤 User Name:</b> {target_user.mention}\n"
            f"<b>🆔 User ID:</b> <code>{target_user.id}</code>\n"
            f"<b>🌐 Username:</b> @{target_user.username or 'None'}\n"
            f"<b>💎 Status:</b> <code>VIP Premium Activated</code>\n"
            f"<b>📅 Joined/Activated Date:</b> <code>{joined_date}</code>\n"
            f"<b>⏳ Expire Date:</b> <code>{expire_date}</code>\n"
            f"<b>🛠️ Added By Admin:</b> {message.from_user.mention}"
        )

        try:
            await client.send_photo(PREMIUM_LOG_CHANNEL, photo=PREMIUM_PIC, caption=premium_log_text)
        except Exception as log_err:
            print(f"Premium Log Error: {log_err}")

        await pro.edit(f"<b>✅ Successfully added user <code>{user_id}</code> to Premium!</b>", reply_markup=reply_markup)
    except Exception as e:
        await pro.edit(f"<b>❌ Error:</b> <code>{e}</code>", reply_markup=reply_markup)


@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def remove_premium_user(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not args:
        return await pro.edit(
            "<b>Please provide a user ID to remove from Premium.</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/remove_premium [user_id]</code>",
            reply_markup=reply_markup
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ Invalid User ID! Please provide a numeric user ID.</b>", reply_markup=reply_markup)

    try:
        # Database se remove premium function call
        if hasattr(db, 'remove_premium'):
            await db.remove_premium(user_id)
        
        await pro.edit(f"<b>⛔️ Successfully removed user <code>{user_id}</code> from Premium.</b>", reply_markup=reply_markup)
    except Exception as e:
        await pro.edit(f"<b>❌ Error:</b> <code>{e}</code>", reply_markup=reply_markup)
