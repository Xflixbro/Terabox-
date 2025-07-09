import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters, idle
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s - %(filename)s:%(lineno)d"
)

logger = logging.getLogger(__name__)


#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "15529802"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "92bcb6aa798a6f1feadbc917fccb54d3")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002825201004"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "821215952"))
ADMINS = [OWNER_ID]

DUMP_CHAT_IDS = os.environ.get('DUMP_CHAT_IDS', '-1002434717011').split()

#Port
PORT = os.environ.get("PORT", "8888")

DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Testrename:Testrename@cluster0.kgwa5zd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "terabox")



TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/0ydLhFQ4/photo-2025-05-30-11-57-11.jpg")
#Collection of pics for Bot // #Optional but atleast one pic link should be replaced if you don't want predefined links
PICS = (os.environ.get("PICS", "https://ibb.co/1GVJ095z https://i.ibb.co/0ydLhFQ4/photo-2025-05-30-11-57-11.jpg https://ibb.co/mFDDrmSH")).split() #Required


OWNER_TAG = os.environ.get("OWNER_TAG", "nyxkings")


BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"

USER_REPLY_TEXT = "❌Don't send me messages directly I'm only Terabox Download Bot!"



LOG_FILE_NAME = "TeraBoxGenie.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
