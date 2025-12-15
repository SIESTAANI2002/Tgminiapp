# ================== CRITICAL ASYNCIO FIX (MUST BE FIRST) ==================
import asyncio

# Force event loop for Python 3.10+
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

# ================== STANDARD IMPORTS ==================
import json
import os
from os import path as ospath, mkdir, system, getenv
from logging import INFO, ERROR, FileHandler, StreamHandler, basicConfig, getLogger
from traceback import format_exc
from asyncio import Queue, Lock

# ================== SAFE UVLOOP (OPTIONAL) ==================
try:
    import uvloop
    uvloop.install()
except Exception:
    pass

# ================== THIRD PARTY ==================
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

# ================== LOGGING ==================
basicConfig(
    format="[%(asctime)s] [%(name)s | %(levelname)s] - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%m/%d/%Y, %H:%M:%S %p",
    handlers=[FileHandler('log.txt'), StreamHandler()],
    level=INFO
)

getLogger("pyrogram").setLevel(ERROR)
LOGS = getLogger(__name__)

# ================== LOAD ENV ==================
load_dotenv('config.env')

# ================== GLOBAL CACHES ==================
ani_cache = {
    'fetch_animes': True,
    'ongoing': set(),
    'completed': set()
}

ffpids_cache = list()

ffLock = Lock()
ffQueue = Queue()
ff_queued = dict()

# ================== VAR CONFIG ==================
class Var:
    API_ID = getenv("API_ID")
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    MONGO_URI = getenv("MONGO_URI")

    if not BOT_TOKEN or not API_HASH or not API_ID or not MONGO_URI:
        LOGS.critical("Important Variables Missing. Fill Up and Retry!")
        exit(1)

    OWNER_ID = int(getenv("OWNER_ID", "123456789"))
    RSS_ITEMS = getenv("RSS_ITEMS", "").split()
    RSS_TOR = getenv("RSS_TOR", "").split()
    FSUB_CHATS = list(map(int, getenv("FSUB_CHATS", "").split()))
    BACKUP_CHANNEL = getenv("BACKUP_CHANNEL") or ""
    MAIN_CHANNEL = int(getenv("MAIN_CHANNEL"))
    LOG_CHANNEL = int(getenv("LOG_CHANNEL", "0"))
    FILE_STORE = int(getenv("FILE_STORE"))
    ADMINS = list(map(int, getenv("ADMINS", "").split()))

    TOKYO_API_KEY = getenv("TOKYO_API_KEY", "")
    TOKYO_USER = getenv("TOKYO_USER", "")
    TOKYO_PASS = getenv("TOKYO_PASS", "")

    WEBSITE = getenv("WEBSITE", "")
    TG_PROTECT_CONTENT = getenv("TG_PROTECT_CONTENT", "False").lower() == "true"
    BOT_USERNAME = getenv("BOT_USERNAME", "")

    SEND_SCHEDULE = getenv("SEND_SCHEDULE", "False").lower() == "true"
    BRAND_UNAME = getenv("BRAND_UNAME", "@username")
    SECOND_BRAND = getenv("SECOND_BRAND", "AnimeToki")

    QUALS = getenv("QUALS", "720 1080").split()

    DRIVE_FOLDER_ID = getenv("DRIVE_FOLDER_ID", "")
    AS_DOC = getenv("AS_DOC", "True").lower() == "true"

    THUMB = getenv("THUMB", "")
    AUTO_DEL = getenv("AUTO_DEL", "True").lower() == "true"
    DEL_TIMER = int(getenv("DEL_TIMER", "600"))

    START_PHOTO = getenv("START_PHOTO", "")
    START_MSG = getenv(
        "START_MSG",
        "<b>Hey {first_name}</b>\n\n<i>I am Auto Anime Encoder Bot!</i>"
    )
    START_BUTTONS = getenv(
        "START_BUTTONS",
        "UPDATES|https://t.me/updates SUPPORT|https://t.me/support"
    )

# ================== INIT FILES/FOLDERS ==================
if Var.THUMB and not ospath.exists("thumb.jpg"):
    system(f"wget -q {Var.THUMB} -O thumb.jpg")
    LOGS.info("Thumbnail downloaded")

for folder in ("encode", "thumbs", "downloads"):
    if not ospath.isdir(folder):
        mkdir(folder)

# ================== BOT INIT ==================
try:
    bot = Client(
        name="AutoAniAdvance",
        api_id=int(Var.API_ID),
        api_hash=Var.API_HASH,
        bot_token=Var.BOT_TOKEN,
        plugins=dict(root="bot/modules"),
        parse_mode=ParseMode.HTML
    )

    bot_loop = bot.loop
    sch = AsyncIOScheduler(timezone="Asia/Kolkata", event_loop=bot_loop)

except Exception as e:
    LOGS.error(str(e))
    exit(1)
