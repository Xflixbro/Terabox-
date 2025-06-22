import asyncio
import logging
import os
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.database import db
from config import *
from plugins.FORMATS import *
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

# Enable logging
logging.basicConfig(level=logging.INFO)

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    
    logging.info(f"Received /start command from user ID: {id}")

    # Check and add user to the database if not present
    if not await db.present_user(id):
        try:
            await db.add_user(id)
        except Exception as e:
            logging.error(f"Error adding user: {e}")

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('🦄 Developer', url='https://t.me/shizukawachan')],
            [InlineKeyboardButton('🗣️ About Me', callback_data="about"),
             InlineKeyboardButton("🔒 Close", callback_data="close")]
        ]
    )
            
    await message.reply_photo(
        photo=START_PIC,
        caption=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name or '',
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
    )

#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""
REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

@Bot.on_message(filters.command('users') & filters.private & filters.user(OWNER_ID))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') )
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

@Bot.on_message(filters.private & filters.command('send'))
async def send_to_user(client: Bot, message: Message):
    if message.reply_to_message:
        # Check if user provided a user ID
        if len(message.command) < 2:
            await message.reply("❌ Please provide a user ID.\n\nUsage: `/send <user_id>` (reply to a message)")
            return
        
        try:
            target_user_id = int(message.command[1])
        except ValueError:
            await message.reply("❌ Invalid user ID. Please provide a valid numeric user ID.")
            return
        
        send_msg = message.reply_to_message
        pls_wait = await message.reply("<i>Sending Message...</i>")
        
        try:
            await send_msg.copy(target_user_id)
            await pls_wait.edit(f"✅ <b>Message sent successfully to user:</b> <code>{target_user_id}</code>")
        except UserIsBlocked:
            await pls_wait.edit(f"❌ <b>Failed to send message:</b> User <code>{target_user_id}</code> has blocked the bot.")
        except InputUserDeactivated:
            await pls_wait.edit(f"❌ <b>Failed to send message:</b> User <code>{target_user_id}</code> account is deactivated.")
        except PeerIdInvalid:
            await pls_wait.edit(f"❌ <b>Failed to send message:</b> Invalid user ID <code>{target_user_id}</code> or user not found.")
        except Exception as e:
            await pls_wait.edit(f"❌ <b>Failed to send message:</b> {str(e)}")
    
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

@Bot.on_message(filters.command('help') & filters.private)
async def help(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("🤖 Oᴡɴᴇʀ", url=f"tg://openmessage?user_id={OWNER_ID}"), 
            InlineKeyboardButton("🥰 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/shizukawachan")
        ]
    ]
    
    try:
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo = FORCE_PIC,
            caption = HELP_TEXT.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup
        )
    except Exception as e:
        return await message.reply(f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @shizukawachan</i></b>\n<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")

@Bot.on_message(filters.command("stats") )
async def stats_command(client, message):
    total_users = await db.full_userbase()
    
    status = f"""<b><u>Bot Stats</u></b>

Total Users: <code>{len(total_users)}</code>"""

    await message.reply(status)
