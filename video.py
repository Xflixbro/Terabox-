# ===============================[ ᴍᴀᴅᴇ ᴡɪᴛʜ 🤍 ʙʏ @ɴʏxɢᴇɴɪᴇ × @sʜɪᴢᴜᴋᴀᴡᴀᴄʜᴀɴ ]==============================
# ᴅᴏɴ'ᴛ sᴇʟʟ • ᴅᴏɴ'ᴛ ᴄʟᴀɪᴍ ᴀs ʏᴏᴜʀs • sᴜᴘᴘᴏʀᴛ: t.me/ɴʏxᴋɪɴɢsᴜᴘᴘᴏʀᴛ • ʀᴇᴘᴏʀᴛ ʙᴜɢs ᴏʀ sᴜɢɢᴇsᴛ ᴛᴏ: @ɴʏxɢᴇɴɪᴇ
# =================================================================================================
# 
import requests
import aria2p
from datetime import datetime
from status import format_progress_bar
import asyncio
import logging
import os
import time
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
# from plugins.autoDelete import delete_message
from config import *
from database.database import db
from bot import *
import aiohttp
import subprocess

# Configure logging to handle Unicode
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

GENIE_API = "http://128.199.108.75:5000/terabox/fetch"


def to_small_caps(text):
    """Convert text to small caps style"""
    small_caps_map = {
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ',
        'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ',
        'Q': 'ǫ', 'R': 'ʀ', 'S': 'ꜱ', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x',
        'Y': 'ʏ', 'Z': 'ᴢ'
    }
    return ''.join(small_caps_map.get(char, char) for char in text)

async def fetch_json(url: str, params: dict = None) -> dict:
    """Fetch JSON data from API"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params, timeout=aiohttp.ClientTimeout(total=100)) as resp:
                response_text = await resp.text()
                if resp.status != 200:
                    logging.error(f"API Error {resp.status}: {response_text}")
                    raise Exception(f"API request failed: HTTP {resp.status}")
                return await resp.json()
        except aiohttp.ClientError as e:
            logging.error(f"Network error: {str(e)}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            logging.error(f"Fetch error: {str(e)}")
            raise Exception(f"API error: {str(e)}")

def ensure_download_folder():
    """Create download folder if it doesn't exist"""
    download_dir = os.path.join(os.getcwd(), "download")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

async def download(url: str, user_id: int, filename: str, reply_msg, user_mention, file_size: int) -> str:
    """Download file using aria2c"""
    download_dir = ensure_download_folder()
    sanitized_filename = filename.replace("/", "_").replace("\\", "_")
    file_path = os.path.join(download_dir, sanitized_filename)
    
    # Add download to aria2c
    download = aria2.add_uris([url], options={
        'dir': download_dir,
        'out': sanitized_filename
    })
    
    start_time = datetime.now()
    last_update_time = time.time()
    
    # Monitor download progress
    while not download.is_complete:
        await asyncio.sleep(2)
        download.update()
        
        if download.status == "error":
            raise Exception(f"Download failed: {download.error_message}")
        
        if time.time() - last_update_time > 2:
            percentage = download.progress
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
            speed = download.download_speed
            eta = download.eta.total_seconds() if download.eta else 0
            
            progress_text = format_progress_bar(
                filename=to_small_caps(filename),
                percentage=percentage,
                done=download.completed_length,
                total_size=download.total_length,
                status=to_small_caps("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ"),
                eta=eta,
                speed=speed,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=download.gid
            )
            try:
                await reply_msg.edit_text(progress_text)
                last_update_time = time.time()
            except Exception:
                pass
    
    return file_path

def generate_thumbnail(video_path: str, output_path: str, time_position: int = 10) -> str:
    """Generate thumbnail from video"""
    try:
        subprocess.run([
            "ffmpeg", "-ss", str(time_position), "-i", video_path,
            "-vframes", "1", "-q:v", "2", "-vf", "scale=320:-1", output_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_path if os.path.exists(output_path) else None
    except Exception:
        return None

def get_video_duration(file_path: str) -> int:
    """Get video duration using ffprobe"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", file_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return int(float(result.stdout.strip()))
    except Exception:
        return 0

async def get_video_dimensions(video_path):
    """Get video width and height using ffprobe"""
    try:
        process = await asyncio.create_subprocess_exec(
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_path,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            output = stdout.decode().strip()
            if 'x' in output:
                width, height = map(int, output.split('x'))
                if width > 0 and height > 0:
                    return width, height
        return 1280, 720
    except Exception:
        return 1280, 720

async def get_video_metadata(video_path):
    """Get comprehensive video metadata"""
    try:
        width, height = await get_video_dimensions(video_path)
        duration = get_video_duration(video_path)
        return width, height, duration
    except Exception:
        return 1280, 720, 0

async def upload_video(client, file_path, video_title, reply_msg, db_channel_id, user_mention, user_id, message):
    """Upload video to Telegram"""
    try:
        # Check if file exists before proceeding
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
            
        file_size = os.path.getsize(file_path)
        start_time = datetime.now()
        last_update_time = time.time()

        # Generate thumbnail and get duration
        thumbnail_path = f"{file_path}.jpg"
        thumbnail_path = generate_thumbnail(file_path, thumbnail_path)
        duration = get_video_duration(file_path)

        # Progress function
        async def progress(current, total):
            nonlocal last_update_time
            if time.time() - last_update_time > 2:
                percentage = (current / total) * 100
                elapsed = (datetime.now() - start_time).total_seconds()
                eta = (total - current) / (current / elapsed) if current > 0 else 0
                speed = current / elapsed if current > 0 else 0
                
                progress_text = format_progress_bar(
                    filename=to_small_caps(video_title),
                    percentage=percentage,
                    done=current,
                    total_size=total,
                    status=to_small_caps("ᴜᴘʟᴏᴀᴅɪɴɢ"),
                    eta=eta,
                    speed=speed,
                    elapsed=elapsed,
                    user_mention=user_mention,
                    user_id=user_id,
                    aria2p_gid=""
                )
                try:
                    await reply_msg.edit_text(progress_text)
                    last_update_time = time.time()
                except Exception:
                    pass

        # Upload to DB channel
        collection_message = await client.send_video(
            chat_id=db_channel_id,
            video=file_path,
            caption=f"{to_small_caps(video_title)}\n👤 {to_small_caps('ʟᴇᴇᴄʜᴇᴅ ʙʏ')} : {user_mention}",
            thumb=thumbnail_path,
            duration=duration,
            supports_streaming=True,
            progress=progress,
            protect_content=False
        )

        # Copy to user
        copied_msg = await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=db_channel_id,
            message_id=collection_message.id
        )


        return collection_message.id

    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return None


async def download_video(url, reply_msg, user_mention, user_id, client, db_channel_id, message, max_retries=3):
    """Download video using VPS API and aria2c"""
    file_path = None
    upload_successful = False
    try:
        logging.info(f"Fetching video info: {url}")

        # Call VPS API
        api_response = await fetch_json(GENIE_API, {"share_url": url})

        if (not api_response or 
            api_response.get("status") != "success" or 
            not api_response.get("data", {}).get("files")):
            raise Exception("Invalid API response format.")

        # Extract file data
        files = api_response["data"]["files"]
        if not files:
            raise Exception("No files found in the link.")

        file_data = files[0]
        download_link = file_data["download_url"]
        video_title = file_data["file_name"]
        file_size = file_data["size_bytes"]
        thumb_url = file_data["thumbnails"]["url2"]

        if file_size == 0:
            raise Exception("Failed to get file size.")

        # Download with retries
        for attempt in range(1, max_retries + 1):
            try:
                file_path = await download(download_link, user_id, video_title, reply_msg, user_mention, file_size)
                break
            except Exception as e:
                if attempt == max_retries:
                    raise e
                await asyncio.sleep(3)

        await reply_msg.edit_text(f"» {to_small_caps('<b>» ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ..!</b>')}")

        # Upload video
        upload_result = await upload_video(client, file_path, video_title, reply_msg, db_channel_id, user_mention, user_id, message)
        
        # Mark upload as successful only if it returns a valid result
        if upload_result is not None:
            upload_successful = True

        return file_path, thumb_url, video_title, None

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None, None, None, None
    
    finally:
        # Delete file after upload to free space - only if upload was successful or file exists
        if file_path and os.path.exists(file_path):
            try:
                # Only delete the reply message if upload was successful
                if upload_successful:
                    await reply_msg.delete()
                
                os.remove(file_path)
                # Also remove thumbnail if exists
                thumb_path = f"{file_path}.jpg"
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
                logging.info(f"File deleted: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete file: {str(e)}")
