# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport

import os
import time
import asyncio
import urllib.parse
from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from database.database import *
from datetime import datetime, timedelta

PAYMENT_LINK = "https://t.me/mrkillersss" 

# Yahan apni asli UPI ID daal dein
UPI_ID = "aloneboy765592@okicici" 

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    print(f"[CB DEBUG] Received callback: {data} from user: {user_id}")

    try:
        # --- 1. RULES ACCEPT GATE HANDLERS ---
        if data == "read_rules":
            await query.answer()
            rules_text = (
                "<blockquote><b>📜 ᴏᴛᴀᴋᴜꜰʟɪx ɴᴇᴛᴡᴏʀᴋ - ᴛᴇʀᴍꜱ & ʀᴜʟᴇꜱ</b>\n\n"
                "1. <i>ʙᴏᴛ ᴩᴀʀ ᴋɪꜱɪ ʙʜɪ ᴛᴀʀᴀʜ ᴋɪ ᴀʙᴜꜱɪᴠᴇ ʟᴀɴɢᴜᴀɢᴇ ᴋᴀ ᴜꜱᴇ ɴᴀ ᴋᴀʀᴇɪɴ.</i>\n"
                "2. <i>ᴠɪᴘ ᴍᴇᴍʙᴇʀꜱʜɪᴩ ꜱʜᴀʀᴇ ᴋᴀʀɴᴀ ʏᴀ ᴍᴜʟᴛɪᴩʟᴇ ᴀᴄᴄᴏᴜɴᴛꜱ ᴩᴀʀ ᴜꜱᴇ ᴋᴀʀɴᴀ ꜱᴛʀɪᴄᴛ ʙʟᴏᴄᴋ ʜᴀɪ.</i>\n"
                "3. <i>ᴩᴀʏᴍᴇɴᴛ ᴋᴀʀɴᴇ ᴋᴇ ʙᴀᴀᴅ ᴠᴀʟɪᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜɪ ᴀᴅᴍɪɴ ᴋᴏ ʙʜᴇᴊᴇɪɴ.</i>\n"
                "4. <i>ʀᴜʟᴇꜱ ᴛᴏᴅɴᴇ ᴩᴀʀ ʙɪɴᴀ ᴡᴀʀɴɪɴɢ ᴋᴇ ʙᴀɴ ᴋᴀʀ diyā ᴊᴀʏᴇɢᴀ.</i>\n\n"
                "<b>ᴋʀɪᴩʏᴀ ᴀᴀɢᴇ ʙᴀᴅʜɴᴇ ᴋᴇ ʟɪʏᴇ 'ɪ ᴀɢʀᴇᴇ' ᴩᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴇɪɴ.</b></blockquote>"
            )
            rules_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ ɪ ᴀɢʀᴇᴇ & ᴄᴏɴᴛɪɴᴜᴇ", callback_data="accept_rules")],
                [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
            ])
            if query.message.photo:
                await query.message.edit_caption(caption=rules_text, reply_markup=rules_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=rules_text, reply_markup=rules_markup, parse_mode=ParseMode.HTML)

        elif data == "accept_rules":
            await db.accept_rules(user_id) # Database mein save karega ki rules accept ho gaye
            await query.answer("🎉 ʀᴜʟᴇꜱ ᴀᴄᴄᴇᴩᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ! ᴇɴᴊᴏʏ ʙᴏᴛ.", show_alert=True)
            query.data = "start"
            return await cb_handler(client, query)

        # --- 2. EXPANDABLE HELP & FAQ MENU HANDLERS ---
        elif data == "help" or data == "faq_menu":
            await query.answer()
            help_text = (
                "<blockquote><b>📚 ʜᴇʟᴩ & ꜰᴀǫ ᴍᴇɴᴜ</b>\n\n"
                "<i>ᴀᴩɴᴀ ꜱᴀᴡᴀʟ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴇɪɴ ɴɪᴄʜᴇ ᴅɪʏᴇ ɢᴀʏᴇ ʙᴜᴛᴛᴏɴꜱ ꜱᴇ:</i></blockquote>"
            )
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ?", callback_data="faq_download"),
                 InlineKeyboardButton("💎 ʜᴏᴡ ᴠɪᴘ ᴡᴏʀᴋꜱ?", callback_data="faq_vip")],
                [InlineKeyboardButton("⚠️ ʟɪɴᴋ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ?", callback_data="faq_link"),
                 InlineKeyboardButton("📞 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url=PAYMENT_LINK)],
                [InlineKeyboardButton('◀️ ʙᴀᴄᴋ', callback_data='start'),
                 InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data='close')]
            ])
            
            if query.message.photo:
                await query.message.edit_caption(caption=help_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=help_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

        elif data == "faq_download":
            await query.answer()
            ans_text = (
                "<blockquote><b>📥 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰɪʟᴇꜱ?</b>\n\n"
                "1. <i>ꜱᴀʙꜱᴇ ᴩᴇʜʟᴇ ʙᴏᴛ ᴋᴇ ᴀɴᴅᴀʀ ᴅɪ ɢᴀʏɪ ꜰɪʟᴇ ʟɪɴᴋ ᴩᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴇɪɴ.</i>\n"
                "2. <i>ᴀɢᴀʀ ᴀᴀᴩᴋᴇ ᴩᴀᴀꜱ ᴀᴄᴛɪᴠᴇ ᴠɪᴩ ᴩʟᴀɴ ʜᴀɪ, ᴛᴏʜ ꜰɪʟᴇ ᴅɪʀᴇᴄᴛ ᴀᴀᴩᴋᴇ ᴅᴍ ᴍᴇɪɴ ᴀᴀ ᴊᴀʏᴇɢɪ.</i>\n"
                "3. <i>ʙɪɴᴀ ᴠɪᴩ ᴋᴇ, ᴀᴀᴩᴋᴏ ᴛᴇᴍᴩᴏʀᴀʀʏ ᴛᴏᴋᴇɴ ᴠᴇʀɪꜰʏ ᴋᴀʀɴᴀ ᴩᴀᴅ ꜱᴀᴋᴛᴀ ʜᴀɪ.</i></blockquote>"
            )
            back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ꜰᴀǫ", callback_data="faq_menu")]])
            if query.message.photo:
                await query.message.edit_caption(caption=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)

        elif data == "faq_vip":
            await query.answer()
            ans_text = (
                "<blockquote><b>💎 ʜᴏᴡ ᴠɪᴘ ᴀᴄᴄᴇꜱꜱ ᴡᴏʀᴋꜱ?</b>\n\n"
                "• <i>ᴠɪᴘ ᴜꜱᴇʀꜱ ᴋᴏ ᴋᴏɪ ᴀᴅꜱ ʏᴀ ᴛᴏᴋᴇɴ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ɴᴀʜɪ ᴋᴀʀɴɪ ᴩᴀᴅᴛɪ.</i>\n"
                "• <i>ꜱᴀᴀʀɪ ꜰɪʟᴇꜱ 1-ᴄʟɪᴄᴋ ᴍᴇɪɴ ᴅɪʀᴇᴄᴛ ᴍɪʟᴛɪ ʜᴀɪɴ.</i>\n"
                "• <i>ᴀᴀᴩ 'ʙᴜʏ ᴠɪᴘ' ʙᴜᴛᴛᴏɴ ᴩᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴋᴇ ᴋᴏɪ ʙʜɪ ᴩʟᴀɴ ᴄʜᴏᴏꜱᴇ ᴋᴀʀ ꜱᴀᴋᴛᴇ ʜᴀɪɴ.</i></blockquote>"
            )
            back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ꜰᴀǫ", callback_data="faq_menu")]])
            if query.message.photo:
                await query.message.edit_caption(caption=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)

        elif data == "faq_link":
            await query.answer()
            ans_text = (
                "<blockquote><b>⚠️ ʟɪɴᴋ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ / ʙʀᴏᴋᴇɴ?</b>\n\n"
                "<i>ᴀɢᴀʀ ᴋᴏɪ ꜰɪʟᴇ ʟɪɴᴋ ᴏᴩᴇɴ ɴᴀʜɪ ʜᴏ ṟahɪ ʏᴀ ꜰɪʟᴇ ᴅᴇʟᴇᴛᴇ ʜᴏ ᴄʜᴜᴋɪ ʜᴀɪ, ᴛᴏʜ ᴛᴜʀᴀɴᴛ ᴀᴅᴍɪɴ ᴋᴏ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴋᴇ ꜱᴀᴛʜ ᴍᴇꜱꜱᴀɢᴇ ʙʜᴇᴊᴇɪɴ. ᴛᴇᴀᴍ ᴊᴀʟᴅɪ ꜰɪx ᴋᴀʀ degi!</i></blockquote>"
            )
            back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ꜰᴀǫ", callback_data="faq_menu")]])
            if query.message.photo:
                await query.message.edit_caption(caption=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=ans_text, reply_markup=back_markup, parse_mode=ParseMode.HTML)

        elif data == "about":
            await query.answer()
            about_text = ABOUT_TXT.format(first=query.from_user.first_name) if 'ABOUT_TXT' in globals() or 'ABOUT_TXT' in locals() else f"<b>ᴀʙᴏᴜᴛ ʙᴏᴛ</b>"
            text = f"<blockquote>{about_text}</blockquote>"
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('◀️ ʙᴀᴄᴋ', callback_data='start'),
                 InlineKeyboardButton('❌ ᴄʟᴏꜱᴇ', callback_data='close')]
            ])
            
            if query.message.photo:
                await query.message.edit_caption(caption=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

        elif data == "start":
            await query.answer()
            start_text = START_MSG.format(
                first=query.from_user.first_name,
                last=query.from_user.last_name or "",
                username=None if not query.from_user.username else '@' + query.from_user.username,
                mention=query.from_user.mention,
                id=query.from_user.id
            ) if 'START_MSG' in globals() or 'START_MSG' in locals() else f"<b>ᴡᴇʟᴄᴏᴍᴇ {query.from_user.first_name}!</b>"

            start_full_text = start_text + "\n\n<blockquote><b>⚠️ ɴᴏᴛᴇ: ᴛʜɪꜱ ɪꜱ ᴀ ᴩᴀɪᴅ/ᴠɪᴩ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ. ʏᴏᴜ ɴᴇᴇᴅ ᴀᴄᴛɪᴠᴇ ᴠɪᴩ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰɪʟᴇꜱ.</b></blockquote>"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ʙᴜʏ ᴠɪᴘ ᴀᴄᴄᴇꜱꜱ", callback_data="buy_vip_cb"),
                 InlineKeyboardButton("👤 ᴍʏ ᴩʟᴀɴ", callback_data="my_plan_cb")],
                [InlineKeyboardButton("📢 ᴜᴩᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Sofi_Backup"),
                 InlineKeyboardButton("🆘 ꜱᴜᴩᴩᴏʀᴛ", url=BAN_SUPPORT)],
                [InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about"),
                 InlineKeyboardButton("📚 ʜᴇʟᴩ", callback_data="faq_menu")],
                [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
            ])

            if query.message.photo:
                await query.message.edit_caption(caption=start_full_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            else:
                try:
                    await query.message.delete()
                except:
                    pass
                await client.send_photo(
                    chat_id=query.message.chat.id,
                    photo=START_PIC,
                    caption=start_full_text,
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML
                )

        elif data in ["buy_vip_cb", "buy_upgrade"]:
            await query.answer()
            plans_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⚡ 7 ᴅᴀʏꜱ (₹30)", callback_data="plan_7d"), InlineKeyboardButton("⚡ 15 ᴅᴀʏꜱ (₹50)", callback_data="plan_15d")],
                    [InlineKeyboardButton("⚡ 1 ᴍᴏɴᴛʜ (₹90)", callback_data="plan_1m"), InlineKeyboardButton("⚡ 3 ᴍᴏɴᴛʜꜱ (₹220)", callback_data="plan_3m")],
                    [InlineKeyboardButton("⚡ ʟɪꜰᴇᴛɪᴍᴇ (₹499)", callback_data="plan_life")],
                    [InlineKeyboardButton("📊 ᴄᴏᴍᴩᴀʀᴇ ᴩʟᴀɴꜱ", callback_data="compare_plans")],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            text = "<blockquote><b>💎 ᴠɪᴩ ᴩʀᴇᴍɪᴜᴍ ᴩʟᴀɴꜱ & ᴩʀɪᴄɪɴɢ 💎</b>\n\n<i>ᴋʀɪᴩʏᴀ ɴɪᴄʜᴇ ꜱᴇ ᴀᴩɴᴀ ᴩᴀꜱᴀɴᴅɪᴅᴀ ᴩʟᴀɴ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴇɪɴ:</i></blockquote>"
            
            if query.message.photo:
                await query.message.edit_caption(caption=text, reply_markup=plans_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=text, reply_markup=plans_markup, parse_mode=ParseMode.HTML)

        # --- 3. VIP PLAN COMPARISON TABLE HANDLER ---
        elif data == "compare_plans":
            await query.answer()
            comparison_text = (
                "<blockquote><b>📊 ᴠɪᴩ ᴩʟᴀɴꜱ ᴄᴏᴍᴩᴀʀɪꜱᴏɴ ᴛᴀʙʟᴇ</b>\n\n"
                "┌──────────────────┬──────────┬──────────┐\n"
                "│ <b>ꜰᴇᴀᴛᴜʀᴇꜱ</b>        │ <b>7 ᴅᴀʏꜱ</b>   │ <b>ʟɪꜰᴇᴛɪᴍᴇ</b> │\n"
                "├──────────────────┼──────────┼──────────┤\n"
                "│ Direct Files     │    ✅    │    ✅    │\n"
                "│ No Ads/Tokens    │    ✅    │    ✅    │\n"
                "│ HD / FHD Quality │    ✅    │    ✅    │\n"
                "│ Price            │   ₹30    │   ₹499   │\n"
                "│ Validity         │  7 Days  │ Unlimited│\n"
                "└──────────────────┴──────────┴──────────┘\n\n"
                "<i>💡 <b>ᴩʀᴏ ᴛɪᴩ:</b> ʟɪꜰᴇᴛɪᴍᴇ ᴩʟᴀɴ ꜱᴀʙꜱᴇ ʙᴇꜱᴛ ᴠᴀʟᴜᴇ deta hai kyunki aapko baar-baar renew karne ki zaroorat nahi padti!</i></blockquote>"
            )
            comp_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ʙᴜʏ ᴠɪᴩ ɴᴏᴡ", callback_data="buy_vip_cb")],
                [InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ᴩʟᴀɴꜱ", callback_data="buy_vip_cb"),
                 InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
            ])
            if query.message.photo:
                await query.message.edit_caption(caption=comparison_text, reply_markup=comp_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=comparison_text, reply_markup=comp_markup, parse_mode=ParseMode.HTML)

        elif data.startswith("plan_"):
            await query.answer()
            plan_info = {
                "plan_7d": ("7 Days Plan", "30", "₹30"),
                "plan_15d": ("15 Days Plan", "50", "₹50"),
                "plan_1m": ("1 Month Plan", "90", "₹90"),
                "plan_3m": ("3 Months Plan", "220", "₹220"),
                "plan_life": ("Lifetime Plan", "499", "₹499")
            }
            plan_name, raw_price, plan_price = plan_info.get(data, ("VIP Plan", "10", "₹10"))
            
            unique_tag = int(time.time())
            upi_uri = f"upi://pay?pa={UPI_ID}&pn=OtakuFlix&am={raw_price}&cu=INR"
            dynamic_qr = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_uri)}&t={unique_tag}"

            expiry_time_str = (datetime.utcnow() + timedelta(hours=5, minutes=35)).strftime("%I:%M:%S %p")
            
            caption_text = (
                f"<blockquote><b>💎 ꜱᴇʟᴇᴄᴛᴇᴅ ᴩʟᴀɴ ᴅᴇᴛᴀɪʟꜱ:</b>\n\n"
                f"<b>📦 ᴩʟᴀɴ:</b> <code>{plan_name}</code>\n"
                f"<b>💰 ᴀᴍᴏᴜɴᴛ:</b> <code>{plan_price} (Auto-Filled)</code>\n\n"
                f"<b>⏳ ǫʀ ᴄᴏᴅᴇ ᴇxᴩɪʀʏ:</b> <code>5 Mins (Expires at {expiry_time_str} IST)</code>\n\n"
                f"<b>📌 ᴩᴀʏᴍᴇɴᴛ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ:</b>\n"
                f"1. <i>Yeh QR code sirf 5 minute ke liye valid hai.</i>\n"
                f"2. <i>Scan karte hi app mein exact <b>{plan_price}</b> automatically aa jayega!</i>\n"
                f"3. <i>Payment ke baad screenshot admin ko bhejein.</i></blockquote>"
            )
            
            qr_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💳 ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴛᴏ ᴀᴅᴍɪɴ", url=PAYMENT_LINK)],
                    [InlineKeyboardButton("🔄 ɢᴇɴᴇʀᴀᴛᴇ ɴᴇᴡ ǫʀ", callback_data=data)],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ᴩʟᴀɴꜱ", callback_data="buy_vip_cb"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            
            try:
                await query.message.delete()
                sent_msg = await client.send_photo(
                    chat_id=query.message.chat.id,
                    photo=dynamic_qr,
                    caption=caption_text,
                    reply_markup=qr_markup,
                    parse_mode=ParseMode.HTML
                )

                async def expire_qr_task(client_obj, chat_id, msg_id):
                    await asyncio.sleep(300)  # 5 Minutes
                    try:
                        expired_caption = (
                            f"<blockquote><b>❌ ǫʀ ᴄᴏᴅᴇ ᴇxᴩɪʀᴇᴅ!</b>\n\n"
                            f"<b>📦 ᴩʟᴀɴ:</b> <code>{plan_name} ({plan_price})</code>\n\n"
                            f"<i>Yeh QR code expire ho chuka hai! Is purane QR par ab payment nahi hoga. Naya fresh QR generate karne ke liye niche button par click karein.</i></blockquote>"
                        )
                        
                        expired_markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("🔄 ɢᴇɴᴇʀᴀᴛᴇ ɴᴇᴡ ꜰʀᴇꜱʜ ǫʀ", callback_data=data)],
                            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ᴩʟᴀɴꜱ", callback_data="buy_vip_cb"),
                             InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                        ])
                        
                        await client_obj.edit_message_media(
                            chat_id=chat_id,
                            message_id=msg_id,
                            media=InputMediaPhoto(
                                media="https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg", 
                                caption=expired_caption, 
                                parse_mode=ParseMode.HTML
                            ),
                            reply_markup=expired_markup
                        )
                    except Exception:
                        pass

                asyncio.create_task(expire_qr_task(client, query.message.chat.id, sent_msg.id))

            except Exception as e:
                await query.answer(f"Error: {e}", show_alert=True)

        elif data == "my_plan_cb":
            await query.answer()
            is_active, expiry = await db.check_paid_access(user_id)
            plan_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💎 ʙᴜʏ / ᴜᴩɢʀᴀᴅᴇ ᴩʟᴀɴ", callback_data="buy_vip_cb")],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            
            if is_active and expiry:
                if isinstance(expiry, datetime):
                    exp_str = expiry.strftime("%d-%b-%Y | %I:%M %p")
                else:
                    exp_str = str(expiry)
                
                text = (
                    f"<blockquote><b>💎 ʏᴏᴜʀ ᴠɪᴩ ᴩʀᴇᴍɪᴜᴍ ᴩʟᴀɴ ɪꜱ ᴀᴄᴛɪᴠᴇ!</b>\n\n"
                    f"<b>👤 ᴜꜱᴇʀ:</b> {query.from_user.mention}\n"
                    f"<b>🆔 ɪᴅ:</b> <code>{user_id}</code>\n"
                    f"<b>⏳ ᴇxᴩɪʀʏ:</b> <code>{exp_str}</code></blockquote>"
                )
            else:
                text = (
                    f"<blockquote><b>❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴩʀᴇᴍɪᴜᴍ ᴩʟᴀɴ.</b>\n\n"
                    f"<i>ɴɪᴄʜᴇ ʙᴜᴛᴛᴏɴ ᴩᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴋᴇ ᴩʟᴀɴꜱ & ᴩʀɪᴄᴇ ᴅᴇᴋʜᴇɪْن!</i></blockquote>"
                )
            
            if query.message.photo:
                await query.message.edit_caption(caption=text, reply_markup=plan_markup, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text=text, reply_markup=plan_markup, parse_mode=ParseMode.HTML)

        elif data == "close":
            await query.answer()
            try:
                await query.message.delete()
                if query.message.reply_to_message:
                    await query.message.reply_to_message.delete()
            except Exception:
                pass

    except Exception as e:
        print(f"[CB ERROR]: {e}")
        try:
            await query.answer(f"ᴇʀʀᴏʀ: {e}", show_alert=True)
        except:
            pass
