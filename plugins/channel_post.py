# ===============================[ ᴍᴀᴅᴇ ᴡɪᴛʜ 🤍 ʙʏ @ɴʏxɢᴇɴɪᴇ × @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ ]==============================
# ᴅᴏɴ'ᴛ sᴇʟʟ • ᴅᴏɴ'ᴛ ᴄʟᴀɪᴍ ᴀs ʏᴏᴜʀs • sᴜᴘᴘᴏʀᴛ: t.me/nyxkingsupport • ʀᴇᴘᴏʀᴛ: @ɴʏxɢᴇɴɪᴇ
# =================================================================================================

from status import format_progress_bar
from video import download_video, upload_video
import asyncio, logging, os
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

from bot import Bot
from config import *
from helper_func import *
from database.database import db
from plugins.FORMATS import *
from plugins.start import *

# 🔒 Only non-command private messages are handled here
@Bot.on_message(filters.private & ~filters.command([
    'start', 'users', 'broadcast', 'stats', 'help', 'cancel', 'short'
]))
async def handle_message(client: Client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    message_text = message.text.strip() if message.text else ""

    # 🔐 Add user to DB if not present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except Exception as e:
            logging.error(f"Failed to add user {user_id}: {e}")

    # 🌐 TeraBox Link Validation
    valid_domains = [
        'terabox.com', 'nephobox.com', '4funbox.com', 'mirrobox.com', 'momerybox.com',
        'teraboxapp.com', '1024tera.com', 'terabox.app', 'gibibox.com', 'goaibox.com',
        'terasharelink.com', 'teraboxlink.com', 'terafileshare.com', 'teraboxshare.com', 'terabox.club'
    ]
    
    if not any(domain in message_text for domain in valid_domains):
        return await message.reply("⚠️ Sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ TᴇʀᴀBᴏx ʟɪɴᴋ.")

    reply_msg = await message.reply_text("<b>» Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ...</b>")

    # Direct download and upload process
    try:
        file_path, thumb, title, duration = await download_video(
            message_text, reply_msg, user_mention, user_id, client, CHANNEL_ID, message
        )
        
        if not file_path:
            return await reply_msg.edit_text("❌ Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴏʀ ᴇᴍᴘᴛʏ ʟɪɴᴋ.")

        # Start upload process
        asyncio.create_task(upload_video(
            client=client,
            file_path=file_path,
            video_title=title,
            reply_msg=reply_msg,
            db_channel_id=CHANNEL_ID,
            user_mention=user_mention,
            user_id=user_id,
            message=message
        ))
        
    except Exception as e:
        logging.error(f"Download error: {e}")
        await reply_msg.edit_text("❌ Eʀʀᴏʀ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ.")
