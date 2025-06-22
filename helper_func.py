#(©)Codexbotz
import binascii
import base64
import re
import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from shortzy import Shortzy
import requests
import time
from datetime import datetime
from database.database import *
from config import OWNER_ID
import random
import string
from datetime import datetime, timedelta
from database.database import db  # Ensure this is the correct import for your database instance
#=============================================================================================================================================================================
# -------------------- HELPER FUNCTIONS FOR USER VERIFICATION IN DIFFERENT CASES -------------------- 
#=============================================================================================================================================================================


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
