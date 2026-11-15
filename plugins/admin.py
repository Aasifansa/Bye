# ᴀ ʙᴏᴛ ɪs ɴᴏᴛ ᴊᴜsᴛ ʟɪɴᴋs ᴀɴᴅ ᴄᴏᴅᴇ, ɪᴛ ɪs ᴛʜᴇ ʙʀɪᴅɢᴇ ʙᴇᴛᴡᴇᴇɴ ᴄᴜʀɪᴏsɪᴛʏ ᴀɴᴅ ᴅɪsᴄᴏᴠᴇʀʏ.
# ❝ ᴛʜᴇ ʙᴇsᴛ ᴡᴀʏ ᴛᴏ ᴘʀᴇᴅɪᴄᴛ ᴛʜᴇ ғᴜᴛᴜʀᴇ ɪs ᴛᴏ ɪɴᴠᴇɴᴛ ɪᴛ, ᴀɴᴅ ᴇᴠᴇʀʏ ʟɪɴᴇ ᴏғ ᴄᴏᴅᴇ ɪs ᴀ sᴛᴇᴘ ɪɴ ᴛʜᴀᴛ ᴅɪʀᴇᴄᴛɪᴏɴ. ❞

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



# ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴs ʙʏ ᴏᴡɴᴇʀ
@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    check = 0
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b><blockquote>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ɪᴅ(s) ᴛᴏ ᴀᴅᴅ ᴀs ᴀᴅᴍɪɴ.</blockquote></b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b>\n"
            "<code>/add_admin [user_id]</code> — ᴀᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜsᴇʀ ɪᴅs\n\n"
            "<b>ᴇxᴀᴍᴘʟᴇ:</b>\n"
            "<code>/add_admin 1234567890 9876543210</code>",
            reply_markup=reply_markup
        )

    admin_list = ""
    for id in admins:
        try:
            id = int(id)
        except:
            admin_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue

        if id in admin_ids:
            admin_list += f"<blockquote><b>ɪᴅ <code>{id}</code> ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs.</b></blockquote>\n"
            continue

        id = str(id)
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(ɪᴅ: <code>{id}</code>) ᴀᴅᴅᴇᴅ.</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"

    if check == len(admins):
        for id in admins:
            await db.add_admin(int(id))
        await pro.edit(f"<b>✅ ᴀᴅᴍɪɴ(s) ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ:</b>\n\n{admin_list}", reply_markup=reply_markup)
    else:
        await pro.edit(
            f"<b>❌ sᴏᴍᴇ ᴇʀʀᴏʀs ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴs:</b>\n\n{admin_list.strip()}\n\n"
            "<b><i>ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</i></b>",
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
            "<b><blockquote>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ᴀᴅᴍɪɴ ɪᴅ(s) ᴛᴏ ʀᴇᴍᴏᴠᴇ.</blockquote></b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b>\n"
            "<code>/deladmin [user_id]</code> — ʀᴇᴍᴏᴠᴇ sᴘᴇᴄɪғɪᴄ ɪᴅs\n"
            "<code>/deladmin all</code> — ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴀᴅᴍɪɴs",
            reply_markup=reply_markup
        )

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await db.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔️ ᴀʟʟ ᴀᴅᴍɪɴ ɪᴅs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ:</b>\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>ɴᴏ ᴀᴅᴍɪɴ ɪᴅs ᴛᴏ ʀᴇᴍᴏᴠᴇ.</blockquote></b>", reply_markup=reply_markup)

    if admin_ids:
        passed = ''
        for admin_id in admins:
            try:
                id = int(admin_id)
            except:
                passed += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{admin_id}</code></b></blockquote>\n"
                continue

            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅ ʀᴇᴍᴏᴠᴇᴅ</blockquote>\n"
            else:
                passed += f"<blockquote><b>ɪᴅ <code>{id}</code> ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴀᴅᴍɪɴ ʟɪsᴛ.</b></blockquote>\n"

        await pro.edit(f"<b>⛔️ ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴀʟ ʀᴇsᴜʟᴛ:</b>\n\n{passed}", reply_markup=reply_markup)
    else:
        await pro.edit("<b><blockquote>ɴᴏ ᴀᴅᴍɪɴ ɪᴅs ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ.</blockquote></b>", reply_markup=reply_markup)


@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ ɴᴏ ᴀᴅᴍɪɴs ғᴏᴜɴᴅ.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ɪᴅ: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await pro.edit(f"<b>⚡ ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴ ʟɪsᴛ:</b>\n\n{admin_list}", reply_markup=reply_markup)


# --- ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴄᴏᴍᴍᴀɴᴅs ---

@Bot.on_message(filters.command('add_premium') & filters.private & admin)
async def add_premium_user(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not args:
        return await pro.edit(
            "<b><blockquote>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ᴀᴅᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ.</blockquote></b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b>\n"
            "<code>/add_premium [user_id]</code>",
            reply_markup=reply_markup
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ! ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅ.</b>", reply_markup=reply_markup)

    try:
        joined_date = datetime.now().strftime("%d-%b-%Y")
        expire_date = datetime.now() + timedelta(days=30)
        formatted_expire = expire_date.strftime("%d-%b-%Y")

        # Database function fix: passing expiry date correctly
        if hasattr(db, 'add_premium'):
            try:
                await db.add_premium(user_id, expire_date)
            except TypeError:
                await db.add_premium(user_id)
        
        try:
            target_user = await client.get_users(user_id)
        except:
            target_user = message.from_user

        premium_log_text = (
            f"<b>⚡ #ᴘʀᴇᴍɪᴜᴍ_ᴜsᴇʀ_ᴀᴅᴅᴇᴅ</b>\n\n"
            f"<b><blockquote>❝ ᴛʜᴇ ʙᴇsᴛ ᴡᴀʏ ᴛᴏ ᴘʀᴇᴅɪᴄᴛ ᴛʜᴇ ғᴜᴛᴜʀᴇ ɪs ᴛᴏ ɪɴᴠᴇɴᴛ ɪᴛ. ❞</b></blockquote>\n\n"
            f"<b>👤 ᴜsᴇʀ ɴᴀᴍᴇ:</b> {target_user.mention}\n"
            f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{target_user.id}</code>\n"
            f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> @{target_user.username or 'ɴᴏɴᴇ'}\n"
            f"<b>💎 sᴛᴀᴛᴜs:</b> <code>ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ</code>\n"
            f"<b>📅 ᴊᴏɪɴᴇᴅ/ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴅᴀᴛᴇ:</b> <code>{joined_date}</code>\n"
            f"<b>⏳ ᴇxᴘɪʀᴇ ᴅᴀᴛᴇ:</b> <code>{formatted_expire}</code>\n"
            f"<b>🛠️ ᴀᴅᴅᴇᴅ ʙʏ ᴀᴅᴍɪɴ:</b> {message.from_user.mention}"
        )

        try:
            await client.send_photo(PREMIUM_LOG_CHANNEL, photo=PREMIUM_PIC, caption=premium_log_text)
        except Exception as log_err:
            print(f"ᴘʀᴇᴍɪᴜᴍ ʟᴏɢ ᴇʀʀᴏʀ: {log_err}")

        await pro.edit(f"<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴜsᴇʀ <code>{user_id}</code> ᴛᴏ ᴘʀᴇᴍɪᴜᴍ!</b>", reply_markup=reply_markup)
    except Exception as e:
        await pro.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup)


@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def remove_premium_user(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not args:
        return await pro.edit(
            "<b><blockquote>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.</blockquote></b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b>\n"
            "<code>/remove_premium [user_id]</code>",
            reply_markup=reply_markup
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ! ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅ.</b>", reply_markup=reply_markup)

    try:
        if hasattr(db, 'remove_premium'):
            await db.remove_premium(user_id)
        
        await pro.edit(f"<b>⛔️ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴜsᴇʀ <code>{user_id}</code> ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.</b>", reply_markup=reply_markup)
    except Exception as e:
        await pro.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup)
                
