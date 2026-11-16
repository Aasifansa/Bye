# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *

BAN_SUPPORT = f"{BAN_SUPPORT}"
PAYMENT_LINK = "https://t.me/mrkillersss" # Yahan apna payment link ya QR chat link daalein


# --- 💎 PLAN CHECK COMMAND (Priority Handler) ---
@Bot.on_message(filters.command(['plan', 'myplan']) & filters.private)
async def check_user_plan_command(client: Client, message: Message):
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


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<blockquote><b>⛔️ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.</b>\n\n"
            "<i>ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴩᴩᴏʀᴛ ɪꜰ yᴏᴜ ᴛʜɪɴᴋ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ.</i></blockquote>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🆘 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴩᴩᴏʀᴛ", url=BAN_SUPPORT)]]
            )
        )
        
    # ✅ Check Force Subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    # Add user if not already present
    is_new_user = False
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
            is_new_user = True
        except:
            pass

    # --- 👤 LOG: User Started Bot (Only First Time) ---
    if is_new_user:
        try:
            current_time = datetime.now().strftime("%d-%b-%Y | %I:%M:%S %p")
            log_text = (
                f"<blockquote><b>🚀 #ɴᴇᴡ_ᴜsᴇʀ_sᴛᴀʀᴛᴇᴅ_ʙᴏᴛ</b>\n\n"
                f"<b>ᴄᴏᴅᴇ ɪs ʟɪᴋᴇ ʜᴜᴍᴏʀ, ɪᴛ ᴡᴏʀᴋs ʙᴇsᴛ</b>\n"
                f"<b>ᴡʜᴇɴ ɪᴛ ɪs ᴇxᴘʀᴇssᴇᴅ ɪɴ sɪᴍᴘʟᴇ ᴡᴏʀᴅs.</b>\n\n"
                f"<b>👤 ᴜsᴇʀ ɴᴀᴍᴇ:</b> {message.from_user.mention}\n"
                f"<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{message.from_user.id}</code>\n"
                f"<b>🌐 ᴜsᴇʀɴᴀᴍᴇ:</b> @{message.from_user.username or 'ɴᴏɴᴇ'}\n"
                f"<b>📅 ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b> <code>{current_time}</code></blockquote>"
            )
            await client.send_message(LOG_CHANNEL, log_text)
        except Exception as e:
            print(f"sᴛᴀʀᴛ ʟᴏɢ ᴇʀʀᴏʀ: {e}")

    # 🚫 PAID CHECK: Check whether user has active paid/VIP access
    is_active, expiry = await db.check_paid_access(user_id)

    # Handle normal message flow (File link click)
    text = message.text
    if len(text) > 7:
        # Agar user ke paas paid access nahi hai aur wo admin bhi nahi hai
        if not is_active and user_id not in ADMINS:
            return await message.reply_text(
                "<blockquote><b>⛔️ ᴩᴀɪᴅ ᴀᴄᴄᴇꜱꜱ ʀᴇqᴜɪʀᴇᴅ!</b>\n\n"
                "<i>ʏᴇ ʙᴏᴛ ᴀʙ <b>ᴩᴀɪᴅ</b> ʜᴏ 🫥ᴜᴋᴀ ʜᴀɪ. ꜰɪʟᴇꜱ ᴋᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴋᴀʀɴᴇ ᴋᴇ ʟɪyᴇ ᴀᴀᴩᴋᴇ ᴩᴀᴀꜱ ᴀᴄᴛɪᴠᴇ <b>ᴠɪᩩ ꜱᴜʙꜱᴄʀɪᴩᴛɪᴏɴ</b> ʜᴏɴᴀ ᴄʜᴀʜɪyᴇ.</i></blockquote>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("💎 ʙᴜʏ ᴠɪᩩ ᴀᴄᴄᴇꜱꜱ", url=PAYMENT_LINK)],
                        [InlineKeyboardButton("👤 ᴄʜᴇᴄᴋ ᴍʏ ᴩʟᴀɴ", callback_data="my_plan_cb")],
                        [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                    ]
                )
            )

        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        # Shareable link for the file
        share_url = f"https://t.me/share/url?url=https://t.me/{client.username}?start={base64_string}"

        codeflix_msgs = []
        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, 
                                             filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                       else ("" if not msg.caption else msg.caption.html))

            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📤 ꜱʜᴀʀᴇ ꜰɪʟᴇ", url=share_url),
                        InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ", callback_data="close")
                    ]
                ]
            ) if not DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")
                pass

        FILE_AUTO_DELETE = await db.get_del_timer()
        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<blockquote><b>⏳ ᴛʜɪꜱ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {get_exp_time(FILE_AUTO_DELETE)}.\nᴩʟᴇᴀꜱᴇ ꜱᴀᴠᴇ ᴏʀ ꜰᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ yᴏᴜʀ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ʙᴇꜰᴏʀᴇ ɪᴛ ɢᴇᴛꜱ ᴅᴇʟᴇᴛᴇᴅ.</b></blockquote>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("♻️ ɢᴇᴛ ꜰɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)],
                        [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
                    ]
                ) if reload_url else None

                await notification_msg.edit(
                    "<blockquote><b>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!\n\nᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ 👇</b></blockquote>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        # Start Menu (Paid Bot Menu Layout)
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💎 ʙᴜʏ ᴠɪᩩ ᴀᴄᴄᴇꜱꜱ", url=PAYMENT_LINK),
                    InlineKeyboardButton("👤 ᴍʏ ᴩʟᴀɴ", callback_data="my_plan_cb")
                ],
                [
                    InlineKeyboardButton("📢 ᴜᴩᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Sofi_Backup"),
                    InlineKeyboardButton("🆘 ꜱᴜᴩᴩᴏʀᴛ", url=BAN_SUPPORT)
                ],
                [
                    InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("📚 ʜᴇʟᴩ", callback_data="help")
                ],
                [
                    InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")
                ]
            ]
        )
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ) + "\n\n<blockquote><b>⚠️ ɴᴏᴛᴇ: ᴛʜɪꜱ ɪꜱ ᴀ ᴩᴀɪᴅ/ᴠɪᩩ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ.\nʏᴏᴜ ɴᴇᴇᴅ ᴀᴄᴛɪᴠᴇ ᴠɪᩩ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰɪʟᴇꜱ.</b></blockquote>",
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586)  # 🔥
        
        return


#=====================================================================================##
chat_data_cache = {}

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ ꜱᴇᴄ..</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link
                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=f"📢 {name}", url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! ᴇʀʀᴏʀ, ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴛᴏ ꜱᴏʟᴠᴇ ᴛʜᴇ ɪꜱꜱᴜᴇꜱ @mrkillersss</i></b>\n"
                        f"<blockquote expandable><b>ʀᴇᴀꜱᴏɴ:</b> {e}</blockquote>"
                    )

        try:
            if message.command and len(message.command) > 1:
                arg_param = message.command[1]
                retry_url = f"https://t.me/{client.username}?start={arg_param}"
            else:
                retry_url = f"https://t.me/{client.username}"

            buttons.append([
                InlineKeyboardButton(
                    text='♻️ ᴛʀy ᴀɢᴀɪɴ',
                    url=retry_url
                ),
                InlineKeyboardButton(
                    text='❓ ʜᴏᴡ ᴛᴏ ᴊᴏɪɴ',
                    callback_data='help'
                )
            ])
        except Exception:
            pass

        await temp.delete()
        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! ᴇʀʀᴏʀ, ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴛᴏ ꜱᴏʟᴠᴇ ᴛʜᴇ ɪꜱꜱᴜᴇꜱ @mrkillersss</i></b>\n"
            f"<blockquote expandable><b>ʀᴇᴀꜱᴏɴ:</b> {e}</blockquote>"
        )


@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about"), InlineKeyboardButton("• ʜᴇʟᴩ •", callback_data="help")],
            [InlineKeyboardButton("• ᴄʟᴏꜱᴇ •", callback_data="close")]
        ]
    )
    await message.reply(text=CMD_TXT, reply_markup=reply_markup, quote=True)
