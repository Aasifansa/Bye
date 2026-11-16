import re
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, LOG_CHANNEL
from database.database import db

def parse_duration(duration_str: str):
    """
    Exact duration parse karega:
    1d = 1 day, 7d = 7 days, 1m = 30 days, 1y = 365 days, 12h = 12 hours
    """
    duration_str = duration_str.lower().strip()
    match = re.match(r"^(\d+)([dhmy]?)$", duration_str)
    if not match:
        return None, None
    
    value = int(match.group(1))
    unit = match.group(2) or "d"

    if unit == "h":
        return timedelta(hours=value), f"{value} Hour(s)"
    elif unit == "d":
        return timedelta(days=value), f"{value} Day(s)"
    elif unit == "m":
        return timedelta(days=value * 30), f"{value} Month(s)"
    elif unit == "y":
        return timedelta(days=value * 365), f"{value} Year(s)"
    return None, None


@Bot.on_message(filters.command(["add_premium", "addpremium", "add_vip"]) & filters.private & filters.user(ADMINS))
async def add_premium_command(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "<blockquote><b>⚠️ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ!</b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b> <code>/add_premium user_id duration</code>\n"
            "<b>ᴇxᴀᴍᴘʟᴇs:</b>\n"
            "• <code>/add_premium 123456789 1d</code> (1 Day)\n"
            "• <code>/add_premium 123456789 7d</code> (7 Days)\n"
            "• <code>/add_premium 123456789 1m</code> (1 Month)\n"
            "• <code>/add_premium 123456789 12h</code> (12 Hours)</blockquote>",
            parse_mode=ParseMode.HTML
        )

    try:
        target_user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("<b>❌ ᴜsᴇʀ ɪᴅ sɪʀꜰ ɴᴜᴍʙᴇʀs ᴍᴇɪɴ ʜᴏɴɪ ᴄʜᴀʜɪʏᴇ!</b>", parse_mode=ParseMode.HTML)

    duration_input = message.command[2]
    delta, plan_label = parse_duration(duration_input)

    if not delta:
        return await message.reply_text(
            "<b>❌ ɢᴀʟᴀᴛ ᴛɪᴍᴇ ꜰᴏʀᴍᴀᴛ!</b>\n<i>Sahi format use karein: 1d, 7d, 15d, 1m, 12h</i>",
            parse_mode=ParseMode.HTML
        )

    status_msg = await message.reply_text("<b>⏳ ᴀᴄᴛɪᴠᴀᴛɪɴɢ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ...</b>", parse_mode=ParseMode.HTML)

    # Exact UTC for DB & IST (UTC + 5:30) for Display
    now_utc = datetime.utcnow()
    expiry_utc = now_utc + delta

    now_ist = now_utc + timedelta(hours=5, minutes=30)
    expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)

    try:
        await db.add_premium(target_user_id, expiry_utc, plan_label)
    except Exception as db_err:
        return await status_msg.edit_text(f"<b>❌ ᴅᴀᴛᴀʙᴀsᴇ ᴇʀʀᴏʀ:</b> <code>{db_err}</code>", parse_mode=ParseMode.HTML)

    # User Details Fetch
    try:
        user_info = await client.get_users(target_user_id)
        user_mention = user_info.mention
        user_full_name = user_info.first_name + (f" {user_info.last_name}" if user_info.last_name else "")
        username_str = f"@{user_info.username}" if user_info.username else "ɴᴏɴᴇ"
    except Exception:
        user_mention = f"<a href='tg://user?id={target_user_id}'>User</a>"
        user_full_name = "VIP Member"
        username_str = "ɴᴏɴᴇ"

    join_date_str = now_ist.strftime("%d-%b-%Y | %I:%M:%S %p")
    exp_date_str = expiry_ist.strftime("%d-%b-%Y | %I:%M:%S %p")

    # 1. Unique VIP Receipt (User ko bhejne ke liye)
    user_receipt = (
        f"<blockquote><b>💎 ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 💎</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>👤 ɴᴀᴍᴇ:</b> {user_full_name}\n"
        f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{target_user_id}</code>\n"
        f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> {username_str}\n"
        f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>📅 ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b>\n<code>{join_date_str} IST</code>\n\n"
        f"<b>⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b>\n<code>{exp_date_str} IST</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>✨ ᴀʙ ᴀᴀᴘ ʙɪɴᴀ ᴋɪsɪ ʀᴜᴋᴀᴡᴀᴛ ᴋᴇ sᴀᴀʀɪ ꜰɪʟᴇs ᴅᴏᴡɴʟᴏᴀᴅ ᴋᴀʀ sᴀᴋᴛᴇ ʜᴀɪɴ!</i></blockquote>"
    )

    user_notified = False
    try:
        await client.send_message(
            chat_id=target_user_id,
            text=user_receipt,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 ᴄʜᴇᴄᴋ ᴍʏ ᴘʟᴀɴ", callback_data="my_plan_cb")]
            ]),
            parse_mode=ParseMode.HTML
        )
        user_notified = True
    except Exception as notify_err:
        print(f"[USER NOTIFY ERROR]: {notify_err}")

    # 2. Log Channel Message
    log_receipt = (
        f"<blockquote><b>👑 #ɴᴇᴡ_ᴠɪᴘ_ᴘʀᴇᴍɪᴜᴍ_ᴀᴅᴅᴇᴅ</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>👤 ᴜsᴇʀ:</b> {user_mention}\n"
        f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{target_user_id}</code>\n"
        f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> {username_str}\n"
        f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>📅 ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ:</b> <code>{join_date_str}</code>\n"
        f"<b>⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ:</b> <code>{exp_date_str}</code>\n"
        f"<b>👮‍♂️ ᴀᴅᴅᴇᴅ ʙʏ:</b> {message.from_user.mention}</blockquote>"
    )

    log_sent = False
    try:
        if LOG_CHANNEL:
            await client.send_message(
                chat_id=int(LOG_CHANNEL),
                text=log_receipt,
                parse_mode=ParseMode.HTML
            )
            log_sent = True
    except Exception as log_err:
        print(f"[LOG CHANNEL ERROR]: {log_err}")

    # 3. Admin Confirmation
    notif_status = "✅ Sent" if user_notified else "❌ Failed (User ne bot start nahi kiya ya block hai)"
    log_status = "✅ Sent" if log_sent else "❌ Failed (LOG_CHANNEL mein bot ko Admin banayein)"

    await status_msg.edit_text(
        f"<blockquote><b>✅ ᴘʀᴇᴍɪᴜᴍ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ!</b>\n\n"
        f"<b>👤 ᴜsᴇʀ:</b> {user_mention} (<code>{target_user_id}</code>)\n"
        f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_label}</code>\n"
        f"<b>⏳ ᴇxᴘɪʀʏ:</b> <code>{exp_date_str}</code>\n\n"
        f"<b>📩 ᴜsᴇʀ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ:</b> {notif_status}\n"
        f"<b>📢 ʟᴏɢ ᴄʜᴀɴɴᴇʟ:</b> {log_status}</blockquote>",
        parse_mode=ParseMode.HTML
    )


@Bot.on_message(filters.command(["remove_premium", "removepremium", "del_vip"]) & filters.private & filters.user(ADMINS))
async def remove_premium_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>ᴜsᴀɢᴇ:</b> <code>/remove_premium user_id</code>", parse_mode=ParseMode.HTML)
    
    try:
        target_user_id = int(message.command[1])
        await db.remove_premium(target_user_id)
        await message.reply_text(f"<b>✅ ᴜsᴇʀ <code>{target_user_id}</code> ᴋᴀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇ ᴋᴀʀ ᴅɪʏᴀ ɢᴀʏᴀ ʜᴀɪ!</b>", parse_mode=ParseMode.HTML)
        try:
            await client.send_message(target_user_id, "<blockquote><b>⚠️ ᴀᴀᴘᴋᴀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴅᴍɪɴ ᴅᴡᴀʀᴀ ʀᴇᴍᴏᴠᴇ ᴋᴀʀ ᴅɪʏᴀ ɢᴀʏᴀ ʜᴀɪ.</b></blockquote>", parse_mode=ParseMode.HTML)
        except:
            pass
    except Exception as e:
        await message.reply_text(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>", parse_mode=ParseMode.HTML)
    
