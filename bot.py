# ===============================[ ᴍᴀᴅᴇ ᴡɪᴛʜ 🤍 ʙʏ @ɴʏxɢᴇɴɪᴇ × @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ ]==============================
# ᴅᴏɴ'ᴛ sᴇʟʟ • ᴅᴏɴ'ᴛ ᴄʟᴀɪᴍ ᴀs ʏᴏᴜʀs • sᴜᴘᴘᴏʀᴛ: t.me/ɴʏxᴋɪɴɢsᴜᴘᴘᴏʀᴛ • ʀᴇᴘᴏʀᴛ ʙᴜɢs: @ɴʏxɢᴇɴɪᴇ
# ==================================================================================================

import asyncio
import os
import sys
import pytz
import pyromod.listen
from datetime import datetime
from flask import Flask
from aiohttp import web
from threading import Thread
import aria2p
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
from pyrogram.enums import ParseMode
import pyrogram.utils
from config import *
from plugins import web_server
from dotenv import load_dotenv

# Minimum allowed channel ID (used to prevent PeerIdInvalid errors)
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Load environment variables
load_dotenv(".env")

# 🌐 Flask App (for uptime monitoring)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ..."

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8788)))

def keep_alive():
    Thread(target=run_flask).start()

# 🇮🇳 Get current time in IST
def get_indian_time():
    return datetime.now(pytz.timezone("Asia/Kolkata"))

# ⚙️ Aria2 RPC Initialization
aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

# 🤖 Pyrogram Bot Class
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"}
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        self.uptime = get_indian_time()
        me = await self.get_me()
        self.username = me.username

        try:
            self.db_channel = await self.get_chat(CHANNEL_ID)
        except Exception as e:
            self.LOGGER(__name__).warning(f"❗ Error: {e}")
            self.LOGGER(__name__).warning(f"🔴 Bot must be admin in DB Channel. Check CHANNEL_ID: {CHANNEL_ID}")
            self.LOGGER(__name__).info("🔻 Bᴏᴛ Sᴛᴏᴘᴘᴇᴅ. ᴄᴏɴᴛᴀᴄᴛ @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ ғᴏʀ sᴜᴘᴘᴏʀᴛ.")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"✅ Bᴏᴛ Rᴜɴɴɪɴɢ ᴀs @{self.username} • ᴍᴀᴅᴇ ʙʏ @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ")

        # 🌐 Start aiohttp web server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        # 🔁 Notify owner on restart

        try:
            startup_message = (
                f"<b>"
                f"» ɢᴇɴɪᴇ sᴛᴀʀᴛᴇᴅ...!\n\n"
                f"<blockquote>» ɢᴏᴅ: <a href='https://t.me/nyxgenie'>s ʜ ɪ ᴢ ᴜ ᴋ ᴀ</a>"
                f"</blockquote></b>"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/shizukawachan")]
            ])
            await self.send_message(
                chat_id=OWNER_ID,
                text=startup_message,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        except:
            pass

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🛑 Bᴏᴛ Sᴛᴏᴘᴘᴇᴅ.")

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info("🚀 Bᴏᴛ ɪs ɴᴏᴡ ʀᴜɴɴɪɴɢ...")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("🧨 Sʜᴜᴛᴛɪɴɢ ᴅᴏᴡɴ...")
        finally:
            loop.run_until_complete(self.stop())

# 🚀 Launch the Bot and Web App
if __name__ == "__main__":
    keep_alive()
    Bot().run()

# ===============================[ ɴʏxᴋɪɴɢ × ʙʏ @ɴʏxɢᴇɴɪᴇ × @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ ]==============================
# ᴘᴀʀᴛ ᴏғ Tᴇʀᴀʙᴏx ᴅᴜᴍᴘ ᴘʀᴏᴊᴇᴄᴛ • sᴜᴘᴘᴏʀᴛ: t.me/ɴʏxᴋɪɴɢsᴜᴘᴘᴏʀᴛ • ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ғᴏʀᴋ, ʙᴜᴛ ᴅᴏɴ'ᴛ ʀᴇsᴇʟʟ
# ==================================================================================================
