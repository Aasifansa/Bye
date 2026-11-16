# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport

from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *
from datetime import datetime

PAYMENT_LINK = "https://t.me/mrkillersss" 
PAYMENT_QR = "https://image.zaw-myo.workers.dev/image/db8410f2-94c7-41ab-acdc-e7e319b0e663"

async def smart_edit(query: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup):
    try:
        if query.message.photo:
            await query.message.edit_caption(caption=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            await query.message.edit_text(text=text, disable_web_page_preview=True, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception:
        try:
            await query.message.edit_text(text=text, disable_web_page_preview=True, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Smart Edit Error: {e}")

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    try:
        if data == "help":
            help_text = HELP_TXT.format(first=query.from_user.first_name) if 'HELP_TXT' in globals() or 'HELP_TXT' in locals() else f"<b>ʜᴇʟᴩ ᴍᴇɴᴜ</b>"
            await smart_edit(
                query,
                text=f"<blockquote>{help_text}</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('◀️ ʙᴀᴄᴋ', callback_data='start'),
                     InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )

        elif data == "about":
            about_text = ABOUT_TXT.format(first=query.from_user.first_name) if 'ABOUT_TXT' in globals() or 'ABOUT_TXT' in locals() else f"<b>ᴀʙᴏᴜᴛ ʙᴏᴛ</b>"
            await smart_edit(
                query,
                text=f"<blockquote>{about_text}</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('◀️ ʙᴀᴄᴋ', callback_data='start'),
                     InlineKeyboardButton('❌ ᴄʟᴏꜱᴇ', callback_data='close')]
                ])
            )

        elif data == "start":
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
                 InlineKeyboardButton("📚 ʜᴇʟᴩ", callback_data="help")],
                [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
            ])

            try:
                if query.message.photo:
                    await query.message.edit_caption(caption=start_full_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
                else:
                    await query.message.delete()
                    await client.send_photo(chat_id=query.message.chat.id, photo=START_PIC, caption=start_full_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            except Exception:
                await smart_edit(query, text=start_full_text, reply_markup=keyboard)

        elif data == "buy_vip_cb":
            plans_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⚡ 7 ᴅᴀʏꜱ (₹30)", callback_data="plan_7d"), InlineKeyboardButton("⚡ 15 ᴅᴀʏꜱ (₹50)", callback_data="plan_15d")],
                    [InlineKeyboardButton("⚡ 1 ᴍᴏɴᴛʜ (₹90)", callback_data="plan_1m"), InlineKeyboardButton("⚡ 3 ᴍᴏɴᴛʜꜱ (₹220)", callback_data="plan_3m")],
                    [InlineKeyboardButton("⚡ ʟɪꜰᴇᴛɪᴍᴇ (₹499)", callback_data="plan_life")],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            text = "<blockquote><b>💎 ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ & ᴘʀɪᴄɪɴɢ 💎</b>\n\n<i>Kripya niche se apna pasandida plan select karein:</i></blockquote>"
            await smart_edit(query, text=text, reply_markup=plans_markup)

        elif data.startswith("plan_"):
            plan_info = {
                "plan_7d": ("7 Days Plan", "₹30"),
                "plan_15d": ("15 Days Plan", "₹50"),
                "plan_1m": ("1 Month Plan", "₹90"),
                "plan_3m": ("3 Months Plan", "₹220"),
                "plan_life": ("Lifetime Plan", "₹499")
            }
            plan_name, plan_price = plan_info.get(data, ("VIP Plan", "As per chart"))
            
            caption_text = (
                f"<blockquote><b>💎 ꜱᴇʟᴇᴄᴛᴇᴅ ᴘʟᴀɴ ᴅᴇᴛᴀɪʟꜱ:</b>\n\n"
                f"<b>📦 ᴘʟᴀɴ:</b> <code>{plan_name}</code>\n"
                f"<b>💰 ᴘʀɪᴄᴇ:</b> <code>{plan_price}</code>\n\n"
                f"<b>📌 ᴘᴀʏᴍᴇɴᴛ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ:</b>\n"
                f"1. <i>Niche diye gaye QR code ko scan karke payment karein.</i>\n"
                f"2. <i>Payment successful hone ke baad screenshot admin ko bhejein.</i></blockquote>"
            )
            
            qr_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💳 ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴛᴏ ᴀᴅᴍɪɴ", url=PAYMENT_LINK)],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ᴘʟᴀɴꜱ", callback_data="buy_vip_cb"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            
            try:
                await query.message.delete()
                await client.send_photo(
                    chat_id=query.message.chat.id,
                    photo=PAYMENT_QR,
                    caption=caption_text,
                    reply_markup=qr_markup,
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await query.answer(f"Error: {e}", show_alert=True)

        elif data == "my_plan_cb":
            is_active, expiry = await db.check_paid_access(user_id)
            plan_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💎 ʙᴜʏ / ᴜᴘɢʀᴀᴅᴇ ᴘʟᴀɴ", callback_data="buy_vip_cb")],
                    [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                ]
            )
            
            if is_active and expiry:
                if isinstance(expiry, datetime):
                    exp_str = expiry.strftime("%d-%b-%Y | %I:%M %p")
                else:
                    exp_str = str(expiry)
                
                text = (
                    f"<blockquote><b>💎 ʏᴏᴜʀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɪꜱ ᴀᴄᴛɪᴠᴇ!</b>\n\n"
                    f"<b>👤 ᴜꜱᴇʀ:</b> {query.from_user.mention}\n"
                    f"<b>🆔 ɪᴅ:</b> <code>{user_id}</code>\n"
                    f"<b>⏳ ᴇxᴘɪʀʏ:</b> <code>{exp_str}</code></blockquote>"
                )
            else:
                text = (
                    f"<blockquote><b>❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ.</b>\n\n"
                    f"<i>ɴɪᴄʜᴇ ʙᴜᴛᴛᴏɴ ᴘᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴋᴇ ᴘʟᴀɴꜱ & ᴘʀɪᴄᴇ ᴅᴇᴋʜᴇɪɴ!</i></blockquote>"
                )
            
            await smart_edit(query, text=text, reply_markup=plan_markup)

        elif data == "close":
            try:
                await query.message.delete()
                if query.message.reply_to_message:
                    await query.message.reply_to_message.delete()
            except Exception:
                pass

        elif data.startswith("rfs_ch_"):
            cid = int(data.split("_")[2])
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏꜰꜰ"
                new_mode = "off" if mode == "on" else "on"
                buttons = [
                    [InlineKeyboardButton(f"ʀᴇq ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                    [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
                ]
                await query.message.edit_text(
                    f"<blockquote><b>ᴄʜᴀɴɴᴇʟ:</b> {chat.title}\n<b>ᴄᴜʀʀᴇɴᴛ ꜰᴏʀᴄᴇ-ꜱᴜʙ ᴍᴏᴅᴇ:</b> {status}</blockquote>",
                    reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML
                )
            except Exception:
                await query.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ᴄʜᴀɴɴᴇʟ ɪɴꜰᴏ", show_alert=True)

        elif data.startswith("rfs_toggle_"):
            cid, action = data.split("_")[2:]
            cid = int(cid)
            mode = "on" if action == "on" else "off"
            await db.set_channel_mode(cid, mode)
            await query.answer(f"ꜰᴏʀᴄᴇ-ꜱᴜʙ ꜱᴇᴛ ᴛᴏ {'ON' if mode == 'on' else 'OFF'}")

            chat = await client.get_chat(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏꜰꜰ"
            new_mode = "off" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇq ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"<blockquote><b>ᴄʜᴀɴɴᴇʟ:</b> {chat.title}\n<b>ᴄᴜʀʀᴇɴᴛ ꜰᴏʀᴄᴇ-ꜱᴜʙ ᴍᴏᴅᴇ:</b> {status}</blockquote>",
                reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML
            )

        elif data == "fsub_back":
            channels = await db.show_channels()
            buttons = []
            for cid in channels:
                try:
                    chat = await client.get_chat(cid)
                    mode = await db.get_channel_mode(cid)
                    status = "🟢" if mode == "on" else "🔴"
                    buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
                except:
                    continue

            await query.message.edit_text(
                "<blockquote><b>ꜱᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛꜱ ꜰᴏʀᴄᴇ-ꜱᴜʙ ᴍᴏᴅᴇ:</b></blockquote>",
                reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML
            )

    except Exception as e:
        print(f"[CB ERROR]: {e}")
        try:
            await query.answer(f"ᴇʀʀᴏʀ: {e}", show_alert=True)
        except:
            pass
        
