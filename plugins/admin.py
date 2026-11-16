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

        id_str = str(id)
        if id_str.isdigit() and len(id_str) >= 8:
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
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]])

    if len(args) < 2:
        return await pro.edit(
            "<blockquote><b>⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ɪᴅ ᴀɴᴅ ᴅᴜʀᴀᴛɪᴏɴ!</b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b> <code>/add_premium [user_id] [duration]</code>\n\n"
            "<b>ᴇxᴀᴍᴘʟᴇs:</b>\n"
            "• <code>/add_premium 123456789 30min</code> (30 ᴍɪɴᴜᴛᴇs)\n"
            "• <code>/add_premium 123456789 2h</code> (2 ʜᴏᴜʀs)\n"
            "• <code>/add_premium 123456789 1d</code> (1 ᴅᴀʏ)\n"
            "• <code>/add_premium 123456789 7d</code> (7 ᴅᴀʏs)\n"
            "• <code>/add_premium 123456789 1m</code> (1 ᴍᴏɴᴛʜ)\n"
            "• <code>/add_premium 123456789 1y</code> (1 ʏᴇᴀʀ)\n"
            "• <code>/add_premium 123456789 lifetime</code> (ʟɪғᴇᴛɪᴍᴇ)</blockquote>",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ! ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅ.</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    duration_str = args[1].lower().strip()
    now_utc = datetime.utcnow()

    # Exact Duration Calculation (UTC based for DB accuracy)
    if duration_str == "lifetime":
        delta = timedelta(days=3650)
        plan_label = "Lifetime VIP"
    elif duration_str.endswith("min"):
        try:
            mins = int(duration_str[:-3])
            delta = timedelta(minutes=mins)
            plan_label = f"{mins} Minute(s)"
        except ValueError:
            return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴍɪɴᴜᴛᴇs ғᴏʀᴍᴀᴛ! (ᴇx: <code>30min</code>)</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif duration_str.endswith("h"):
        try:
            hrs = int(duration_str[:-1])
            delta = timedelta(hours=hrs)
            plan_label = f"{hrs} Hour(s)"
        except ValueError:
            return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ʜᴏᴜʀs ғᴏʀᴍᴀᴛ! (ᴇx: <code>2h</code>)</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif duration_str.endswith("d"):
        try:
            days = int(duration_str[:-1])
            delta = timedelta(days=days)
            plan_label = f"{days} Day(s)"
        except ValueError:
            return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴅᴀʏs ғᴏʀᴍᴀᴛ! (ᴇx: <code>1d</code>, <code>7d</code>)</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif duration_str.endswith("mo") or duration_str.endswith("m"):
        try:
            mos = int(duration_str[:-2]) if duration_str.endswith("mo") else int(duration_str[:-1])
            delta = timedelta(days=mos * 30)
            plan_label = f"{mos} Month(s)"
        except ValueError:
            return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴍᴏɴᴛʜ ғᴏʀᴍᴀᴛ! (ᴇx: <code>1m</code>, <code>3m</code>)</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif duration_str.endswith("y"):
        try:
            yrs = int(duration_str[:-1])
            delta = timedelta(days=yrs * 365)
            plan_label = f"{yrs} Year(s)"
        except ValueError:
            return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ʏᴇᴀʀ ғᴏʀᴍᴀᴛ! (ᴇx: <code>1y</code>)</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    elif duration_str.isdigit():
        # Agar sirf number diya ho (jaise 1 ya 7), toh exact utne hi days milenge
        days = int(duration_str)
        delta = timedelta(days=days)
        plan_label = f"{days} Day(s)"
    else:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ! ᴜsᴇ: <code>1d</code>, <code>7d</code>, <code>1m</code>, <code>12h</code></b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    expire_utc = now_utc + delta

    # Indian Standard Time (IST = UTC + 5:30) Display ke liye
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    expire_ist = expire_utc + timedelta(hours=5, minutes=30)

    joined_str = now_ist.strftime("%d-%b-%Y | %I:%M:%S %p")
    expire_str = "ʟɪғᴇᴛɪᴍᴇ (ᴜɴʟɪᴍɪᴛᴇᴅ)" if duration_str == "lifetime" else expire_ist.strftime("%d-%b-%Y | %I:%M:%S %p")

    try:
        # Database mein exact UTC expiry save karein
        try:
            await db.add_premium(user_id, expire_utc, plan_label)
        except TypeError:
            await db.add_premium(user_id, expire_utc)

        # User ki details nikalna
        try:
            target_user = await client.get_users(user_id)
            user_mention = target_user.mention
            user_name = target_user.first_name + (f" {target_user.last_name}" if target_user.last_name else "")
            user_username = f"@{target_user.username}" if target_user.username else "ɴᴏɴᴇ"
        except Exception:
            user_mention = f"<a href='tg://user?id={user_id}'>VIP User</a>"
            user_name = "VIP Member"
            user_username = "ɴᴏɴᴇ"

        # 1. User ko Unique VIP Receipt bhejna
        user_receipt = (
            f"<blockquote><b>💎 ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 💎</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>👤 ɴᴀᴍᴇ:</b> {user_name}\n"
            f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>\n"
            f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> {user_username}\n"
            f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>📅 ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b>\n<code>{joined_str} IST</code>\n\n"
            f"<b>⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b>\n<code>{expire_str} IST</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>✨ ᴀʙ ᴀᴀᴘ ʙɪɴᴀ ᴋɪsɪ ʀᴜᴋᴀᴡᴀᴛ ᴋᴇ sᴀᴀʀɪ ғɪʟᴇs ᴅᴏᴡɴʟᴏᴀᴅ ᴋᴀʀ sᴀᴋᴛᴇ ʜᴀɪɴ!</i></blockquote>"
        )

        user_notified = False
        try:
            await client.send_message(
                chat_id=user_id,
                text=user_receipt,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👤 ᴄʜᴇᴄᴋ ᴍʏ ᴘʟᴀɴ", callback_data="my_plan_cb")]]),
                parse_mode=ParseMode.HTML
            )
            user_notified = True
        except Exception as u_err:
            print(f"[USER NOTIFY ERROR]: {u_err}")

        # 2. Log Channel mein Unique VIP Log bhejna
        premium_log_text = (
            f"<blockquote><b>⚡ #ᴘʀᴇᴍɪᴜᴍ_ᴜsᴇʀ_ᴀᴅᴅᴇᴅ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>👤 ᴜsᴇʀ ɴᴀᴍᴇ:</b> {user_mention}\n"
            f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>\n"
            f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> {user_username}\n"
            f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>📅 ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b> <code>{joined_str}</code>\n"
            f"<b>⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b> <code>{expire_str}</code>\n"
            f"<b>🛠️ ᴀᴅᴅᴇᴅ ʙʏ ᴀᴅᴍɪɴ:</b> {message.from_user.mention}</blockquote>"
        )

        log_sent = False
        target_log_channel = globals().get("PREMIUM_LOG_CHANNEL") or globals().get("LOG_CHANNEL")
        target_pic = globals().get("PREMIUM_PIC")

        if target_log_channel:
            try:
                if target_pic:
                    await client.send_photo(int(target_log_channel), photo=target_pic, caption=premium_log_text, parse_mode=ParseMode.HTML)
                else:
                    await client.send_message(int(target_log_channel), text=premium_log_text, parse_mode=ParseMode.HTML)
                log_sent = True
            except Exception as log_err:
                print(f"[PREMIUM LOG ERROR]: {log_err}")
                try:
                    # Fallback text message agar photo URL fail ho jaye
                    await client.send_message(int(target_log_channel), text=premium_log_text, parse_mode=ParseMode.HTML)
                    log_sent = True
                except Exception as fallback_err:
                    print(f"[LOG FALLBACK ERROR]: {fallback_err}")

        # 3. Admin ko Final Status
        u_stat = "✅ Sent" if user_notified else "❌ Failed (User ne bot start nahi kiya ya block hai)"
        l_stat = "✅ Sent" if log_sent else "❌ Failed (Log Channel ID / Bot Admin check karein)"

        await pro.edit(
            f"<blockquote><b>✅ ᴘʀᴇᴍɪᴜᴍ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ!</b>\n\n"
            f"<b>👤 ᴜsᴇʀ:</b> {user_mention} (<code>{user_id}</code>)\n"
            f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
            f"<b>📅 ᴊᴏɪɴɪɴɢ:</b> <code>{joined_str}</code>\n"
            f"<b>⏳ ᴇxᴘɪʀʏ:</b> <code>{expire_str}</code>\n\n"
            f"<b>📩 ᴜsᴇʀ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ:</b> {u_stat}\n"
            f"<b>📢 ʟᴏɢ ᴄʜᴀɴɴᴇʟ:</b> {l_stat}</blockquote>",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await pro.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def remove_premium_user(client: Client, message: Message):
    pro = await message.reply("<b><i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    args = message.text.split()[1:]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]])

    if not args:
        return await pro.edit(
            "<blockquote><b>⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.</b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b> <code>/remove_premium [user_id]</code></blockquote>",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    try:
        user_id = int(args[0])
    except ValueError:
        return await pro.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ! ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅ.</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    try:
        if hasattr(db, 'remove_premium'):
            await db.remove_premium(user_id)
        
        try:
            await client.send_message(
                chat_id=user_id,
                text="<blockquote><b>⚠️ ᴀᴀᴘᴋᴀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴅᴍɪɴ ᴅᴡᴀʀᴀ ʀᴇᴍᴏᴠᴇ ᴋᴀʀ ᴅɪʏᴀ ɢᴀʏᴀ ʜᴀɪ.</b></blockquote>",
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass

        await pro.edit(f"<b>⛔️ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴜsᴇʀ <code>{user_id}</code> ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception as e:
        await pro.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
