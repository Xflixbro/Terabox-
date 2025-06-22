"""
ᴅᴀᴛᴀʙᴀꜱᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴍᴏᴅᴜʟᴇ
ᴄʀᴇᴀᴛᴇᴅ ʙʏ @ɴʏxɢᴇɴɪᴇ ᴏɴ ᴛɢ
ꜰᴏʀ ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ: ᴛ.ᴍᴇ/ɴʏxᴋɪɴɢꜱᴜᴘᴘᴏʀᴛ
ᴅᴏ ɴᴏᴛ ꜱᴇʟʟ — ᴍᴀᴅᴇ ᴡɪᴛʜ ʟᴏᴠᴇ 💙
"""

import time
import pymongo
import motor
import motor.motor_asyncio

import os
import logging
from datetime import datetime, timedelta
from config import DB_URI, DB_NAME
from bot import Bot

# ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ ᴄʟɪᴇɴᴛ (sʏɴᴄ ᴄʟɪᴇɴᴛ)
dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

logging.basicConfig(level=logging.INFO)

# ᴍᴏɴɢᴏ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ꜰᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀs
collection = database['premium-users']

# ᴅᴇꜰᴀᴜʟᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ ᴛᴇᴍᴘʟᴀᴛᴇ
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

# ɢᴇɴᴇʀᴀᴛᴇ ɴᴇᴡ ᴜꜱᴇʀ ᴅɪᴄᴛ ᴡɪᴛʜ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴅᴀᴛᴀ
def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }


class NyxGenie:
    """
    ᴀꜱʏɴᴄ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄʟᴀꜱꜱ ᴜꜱɪɴɢ ᴍᴏᴛᴏʀ ᴀꜱʏɴᴄɪᴏ
    ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴅɪꜰꜰᴇʀᴇɴᴛ ᴄᴏʟʟᴇᴄᴛɪᴏɴꜱ ᴀɴᴅ ᴅᴀᴛᴀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ
    """

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.database = self.dbclient[DB_NAME]

        # ᴄᴏʟʟᴇᴄᴛɪᴏɴs
        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.user_data = self.database['users']
        self.banned_user_data = self.database['banned_user']
        self.autho_user_data = self.database['autho_user']


    # ᴜꜱᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ
    # ————————————————

    async def present_user(self, user_id: int):
        """Check if user exists"""
        found = await self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        """Add new user"""
        await self.user_data.insert_one({'_id': user_id})

    async def full_userbase(self):
        """Get list of all user IDs"""
        user_docs = await self.user_data.find().to_list(length=None)
        return [doc['_id'] for doc in user_docs]

    async def del_user(self, user_id: int):
        """Delete user"""
        await self.user_data.delete_one({'_id': user_id})


    # ————————————————
    # ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ
    # ————————————————

    async def channel_exist(self, channel_id: int):
        found = await self.channel_data.find_one({'_id': channel_id})
        return bool(found)

    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.channel_data.insert_one({'_id': channel_id})

    async def del_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.channel_data.delete_one({'_id': channel_id})

    async def get_all_channels(self):
        channel_docs = await self.channel_data.find().to_list(length=None)
        return [doc['_id'] for doc in channel_docs]

# ᴅʙ ᴇxᴀᴍᴘʟᴇ ɪɴsᴛᴀɴᴄᴇ
db = NyxGenie(DB_URI, DB_NAME)
