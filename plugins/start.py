# ᴀ ʙᴏᴛ ɪs ɴᴏᴛ ᴊᴜsᴛ ʟɪɴᴋs ᴀɴᴅ ᴄᴏᴅᴇ, ɪᴛ ɪs ᴛʜᴇ ʙʀɪᴅɢᴇ ʙᴇᴛᴡᴇᴇɴ ᴄᴜʀɪᴏsɪᴛʏ ᴀɴᴅ ᴅɪsᴄᴏᴠᴇʀʏ.
# ❝ ᴛʜᴇ ʙᴇsᴛ ᴡᴀʏ ᴛᴏ ᴘʀᴇᴅɪᴄᴛ ᴛʜᴇ ғᴜᴛᴜʀᴇ ɪs ᴛᴏ ɪɴᴠᴇɴᴛ ɪᴛ, ᴀɴᴅ ᴇᴠᴇʀʏ ʟɪɴᴇ ᴏғ ᴄᴏᴅᴇ ɪs ᴀ sᴛᴇᴘ ɪɴ ᴛʜᴀᴛ ᴅɪʀᴇᴄᴛɪᴏɴ. ❞

import asyncio
import os
import random
import re
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
            admin_list += f"<b><blockquote>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"

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
    full_text = message.text.text if hasattr(message.text, 'text') else message.text
    args = full_text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if len(args) < 1:
        return await pro.edit(
            "<b><blockquote>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴀɴᴅ ᴅᴜʀᴀᴛɪᴏɴ.\n\n"
            "ᴜsᴀɢᴇ:\n"
            "<code>/add_premium [user_id] [duration]</code>\n\n"
            "ᴇxᴀᴍᴘʟᴇs:\n"
            "• <code>/add_premium 123456789 10 minutes</code>\n"
            "• <code>/add_premium 123456789 2 hours</code>\n"
            "• <code>/add_premium 123456789 7 days</code>\n"
            "• <code>/add_premium 123456789 1 month</code>\n"
            "• <code>/add_premium 123456789 1 year</code>\n"
            "• <code>/add_premium 123456789 lifetime</code></blockquote></b>",
            reply_markup=reply_markup
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ! ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅ.</b>", reply_markup=reply_markup)

    # Combine remaining args to handle spaces like "10 minutes" or "1 month"
    duration_str = " ".join(args[1:]).lower() if len(args) > 1 else "1 month"
    now = datetime.now()

    if "lifetime" in duration_str or "unlimited" in duration_str:
        expire_date = now + timedelta(days=3650)
        formatted_expire = "ʟɪғᴇᴛɪᴍᴇ (ᴜɴʟɪᴍɪᴛᴇᴅ)"
    else:
        # Regex to extract number and unit
        match = re.search(r'(\d+)\s*([a-zA-Z]+)', duration_str)
        if match:
            num = int(match.group(1))
            unit = match.group(2)

            if unit.startswith('min'):
                expire_date = now + timedelta(minutes=num)
                formatted_expire = expire_date.strftime("%d-%b-%Y | %I:%M %p")
            elif unit.startswith('hour') or unit == 'h':
                expire_date = now + timedelta(hours=num)
                formatted_expire = expire_date.strftime("%d-%b-%Y | %I:%M %p")
            elif unit.startswith('day') or unit == 'd':
                expire_date = now + timedelta(days=num)
                formatted_expire = expire_date.strftime("%d-%b-%Y")
            elif unit.startswith('month') or unit.startswith('mo') or unit == 'm':
                expire_date = now + timedelta(days=num * 30)
                formatted_expire = expire_date.strftime("%d-%b-%Y")
            elif unit.startswith('year') or unit == 'y':
                expire_date = now + timedelta(days=num * 365)
                formatted_expire = expire_date.strftime("%d-%b-%Y")
            else:
                expire_date = now + timedelta(days=30)
                formatted_expire = expire_date.strftime("%d-%b-%Y")
        else:
            expire_date = now + timedelta(days=30)
            formatted_expire = expire_date.strftime("%d-%b-%Y")

    joined_date = now.strftime("%d-%b-%Y")

    try:
        if hasattr(db, 'add_premium'):
            try:
                await db.add_premium(user_id, expire_date)
            except TypeError:
                await db.add_premium(user_id)
        
        try:
            target_user = await client.get_users(user_id)
        except:
            target_user = message.from_user

        # Log Channel Message Text (Small Caps + Single Blockquote)
        premium_log_text = (
            f"<blockquote><b>⚡ #ᴘʀᴇᴍɪᴜᴍ_ᴜsᴇʀ_ᴀᴅᴅᴇᴅ</b>\n\n"
            f"<b>ᴄᴏᴅᴇ ɪs ʟɪᴋᴇ ʜᴜᴍᴏʀ, ɪᴛ ᴡᴏʀᴋs ʙᴇsᴛ</b>\n"
            f"<b>ᴡʜᴇɴ ɪᴛ ɪs ᴇxᴘʀᴇssᴇᴅ ɪɴ sɪᴍᴘʟᴇ ᴡᴏʀᴅs.</b>\n\n"
            f"<b>👤 ᴜsᴇʀ ɴᴀᴍᴇ:</b> {target_user.mention}\n"
            f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{target_user.id}</code>\n"
            f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> @{target_user.username or 'ɴᴏɴᴇ'}\n"
            f"<b>💎 sᴛᴀᴛᴜs:</b> <code>ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ</code>\n"
            f"<b>📅 ᴊᴏɪɴᴇᴅ/ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴅᴀᴛᴇ:</b> <code>{joined_date}</code>\n"
            f"<b>⏳ ᴇxᴘɪʀᴇ ᴅᴀᴛᴇ:</b> <code>{formatted_expire}</code>\n"
            f"<b>🛠️ ᴀᴅᴅᴇᴅ ʙʏ ᴀᴅᴍɪɴ:</b> {message.from_user.mention}</blockquote>"
        )

        try:
            await client.send_message(PREMIUM_LOG_CHANNEL, premium_log_text)
        except Exception as log_err:
            print(f"ᴘʀᴇᴍɪᴜᴍ ʟᴏɢ ᴇʀʀᴏʀ: {log_err}")

        # Send Notification to User DM
        user_notification_text = (
            f"<blockquote><b>🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! ʏᴏᴜʀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ɪs ᴀᴄᴛɪᴠᴀᴛᴇᴅ.</b>\n\n"
            f"<b>💎 sᴛᴀᴛᴜs:</b> <code>ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ</code>\n"
            f"<b>📅 ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴅᴀᴛᴇ:</b> <code>{joined_date}</code>\n"
            f"<b>⏳ ᴇxᴘɪʀᴇ ᴅᴀᴛᴇ:</b> <code>{formatted_expire}</code>\n\n"
            f"<i>ᴇɴᴊᴏʏ ᴜɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇ ᴀᴄᴄᴇss!</i></blockquote>"
        )
        try:
            await client.send_message(user_id, user_notification_text)
        except Exception as user_err:
            print(f"ᴜsᴇʀ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴇʀʀᴏʀ: {user_err}")

        await pro.edit(f"<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴜsᴇʀ <code>{user_id}</code> ᴛᴏ ᴘʀᴇᴍɪᴜᴍ & ɴᴏᴛɪғɪᴇᴅ!</b>", reply_markup=reply_markup)
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


@Bot.on_message(filters.command(['plan', 'myplan']) & filters.private)
async def check_user_plan(client: Client, message: Message):
    user_id = message.from_user.id
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]])

    try:
        is_active, expiry = await db.check_paid_access(user_id)
        if is_active:
            if isinstance(expiry, datetime):
                exp_str = expiry.strftime("%d-%b-%Y | %I:%M %p")
            else:
                exp_str = str(expiry)
            
            await message.reply(
                f"<blockquote><b>💎 ʏᴏᴜʀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɪs ᴀᴄᴛɪᴠᴇ!</b>\n\n"
                f"<b>👤 ᴜsᴇʀ:</b> {message.from_user.mention}\n"
                f"<b>🆔 ɪᴅ:</b> <code>{user_id}</code>\n"
                f"<b>⏳ ᴇxᴘɪʀʏ:</b> <code>{exp_str}</code></blockquote>",
                reply_markup=reply_markup,
                quote=True
            )
        else:
            await message.reply(
                f"<blockquote><b>❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ.</b>\n\n"
                f"<i>ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ʙᴜʏ ᴠɪᴘ ᴀᴄᴄᴇss!</i></blockquote>",
                reply_markup=reply_markup,
                quote=True
            )
    except Exception as e:
        await message.reply(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup, quote=True)


@Bot.on_message(filters.command(['premium_users', 'premium_user']) & filters.private & admin)
async def get_premium_users_list(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]])

    try:
        # Assuming db has a method to fetch premium users, or fetching via collection
        premium_users = []
        if hasattr(db, 'get_all_prem_users'):
            premium_users = await db.get_all_prem_users()
        elif hasattr(db, 'col'):
            async for user in db.col.find({"expires_at": {"$gt": datetime.now()}}):
                premium_users.append(user)

        if not premium_users:
            return await pro.edit("<b><blockquote>❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ғᴏᴜɴᴅ.</blockquote></b>", reply_markup=reply_markup)

        text = "<b>⚡ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʟɪsᴛ:</b>\n\n"
        for u in premium_users:
            uid = u.get('user_id') or u.get('_id')
            exp = u.get('expires_at', 'N/A')
            text += f"• <code>{uid}</code> — ᴇxᴘɪʀᴇs: <code>{exp}</code>\n"

        await pro.edit(f"<blockquote>{text}</blockquote>", reply_markup=reply_markup)
    except Exception as e:
        await pro.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup)
