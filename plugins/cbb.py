#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *
from datetime import datetime

# Ultra-safe smart edit helper (Photo/Text dono ke liye 100% working)
async def smart_edit(query: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup):
    try:
        if query.message.photo:
            await query.message.edit_caption(
                caption=text,
                reply_markup=reply_markup
            )
        else:
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
    except Exception:
        # Fallback agar media state mismatch ho jaye
        try:
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Smart Edit Error: {e}")

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    try:
        if data == "help":
            help_text = HELP_TXT.format(first=query.from_user.first_name) if 'HELP_TXT' in globals() else "<b>ʜᴇʟᴩ ᴍᴇɴᴜ</b>"
            await smart_edit(
                query,
                text=f"<blockquote>{help_text}</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )

        elif data == "about":
            about_text = ABOUT_TXT.format(first=query.from_user.first_name) if 'ABOUT_TXT' in globals() else "<b>ᴀʙᴏᴜᴛ ʙᴏᴛ</b>"
            await smart_edit(
                query,
                text=f"<blockquote>{about_text}</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton('❌ ᴄʟᴏꜱᴇ', callback_data='close')]
                ])
            )

        elif data == "start":
            start_text = START_MSG.format(
                first=query.from_user.first_name,
                last=query.from_user.last_name,
                username=None if not query.from_user.username else '@' + query.from_user.username,
                mention=query.from_user.mention,
                id=query.from_user.id
            ) if 'START_MSG' in globals() else "<b>ᴡᴇʟᴄᴏᴍᴇ!</b>"

            await smart_edit(
                query,
                text=start_text + "\n\n<blockquote><b>⚠️ ɴᴏᴛᴇ: ᴛʜɪꜱ ɪꜱ ᴀ ᴩᴀɪᴅ/ᴠɪᴩ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ. ʏᴏᴜ ɴᴇᴇᴅ ᴀᴄᴛɪᴠᴇ ᴠɪᴩ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰɪʟᴇꜱ.</b></blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💎 ʙᴜʏ ᴠɪᴩ ᴀᴄᴄᴇꜱꜱ", url="https://t.me/mrkillersss"),
                     InlineKeyboardButton("👤 ᴍʏ ᴩʟᴀɴ", callback_data="my_plan_cb")],
                    [InlineKeyboardButton("📚 ʜᴇʟᴩ", callback_data='help'),
                     InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data='about')],
                    [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )

        elif data == "my_plan_cb":
            is_active, expiry = await db.check_paid_access(user_id)
            
            if is_active and expiry:
                time_left = expiry - datetime.utcnow()
                days_left = time_left.days
                hours_left = time_left.seconds // 3600
                
                text = (
                    f"🌟 ʏᴏᴜʀ ᴠɪᴩ ꜱᴜʙꜱᴄʀɪᴩᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ 🌟\n\n"
                    f"• ᴩʟᴀɴ: ᴠɪᴩ ᴩᴀɪᴅ ᴍᴇᴍʙᴇʀ\n"
                    f"• ꜱᴛᴀᴛᴜꜱ: ᴀᴄᴛɪᴠᴇ ✅\n"
                    f"• ᴛɪᴍᴇ ʟᴇꜰᴛ: {days_left} ᴅᴀyꜱ, {hours_left} ʜᴏᴜʀꜱ\n"
                    f"• ᴇxᴩɪʀy (ᴜᴛᴄ): {expiry.strftime('%Y-%m-%d %H:%M')}"
                )
            else:
                text = (
                    f"👤 ᴀᴄᴄᴏᴜɴᴛ ᴩʟᴀɴ: ꜰʀᴇᴇ / ᴜɴᴩᴀɪᴅ\n\n"
                    f"❌ ꜱᴛᴀᴛᴜꜱ: ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴩ ᴩʟᴀɴ ⚠️\n\n"
                    f"ꜰɪʟᴇꜱ ᴅᴏᴡɴʟᴏᴀᴅ ᴋᴀʀɴᴇ ᴋᴇ ʟɪyᴇ ᴩʟᴇᴀꜱᴇ ᴠɪᴩ ᴀᴄᴄᴇꜱꜱ ᴩᴜʀᴄʜᴀꜱᴇ ᴋᴀʀᴇɪɴ."
                )
            
            await query.answer(text, show_alert=True)

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
                    reply_markup=InlineKeyboardMarkup(buttons)
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
                reply_markup=InlineKeyboardMarkup(buttons)
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
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    except Exception as e:
        print(f"[CB ERROR]: {e}")
        try:
            await query.answer(f"ᴇʀʀᴏʀ: {e}", show_alert=True)
        except:
            pass
