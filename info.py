import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/2e2a07e86066538ed7406.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', 'ð ð·ð´ð»ð¾ {user}\n\nØ¨ÙØª ÙÙÙ{bot},\nÙÙØ· Ø§ÙØªØ¨ Ø§Ø³Ù Ø§ÙÙØ³ÙØ³Ù ÙÙØ§ ÙØ³ÙÙ Ø§Ø±Ø³ÙÙ ÙÙ')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "â ï¸ ððð® {query}! ðððð©'ð¨ ðð¤ð© ðð¤ð§ ðð¤ðª. ðð¡ððð¨ð ððð¦ðªðð¨ð© ðð¤ðªð§ ðð¬ð£")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', 'ÙØ±Ø¬Ù Ø§ÙØ§Ø´ØªØ±Ù ÙÙ Ø§ÙÙÙØ§Ø© ÙØ§Ø³ØªØ®Ø¯Ø§Ù Ø§ÙØ¨ÙØª')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "Hai {user}\nwelcome to {chat}")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "False")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'ArrowFlix Discussion | Series & Movies')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "False")
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<code>{file_caption}</code> \n\nâ² [ÙØ³ÙØ³ÙØ§Øª Ø±ÙØ¶Ø§Ù](https://t.me/RamadanTv_2023)\nâ² [Ø¬Ø±ÙØ¨ Ø§ÙØ·ÙØ¨Ø§Øª](https://t.me/RamadanTv2023)</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", "<code>{file_caption}</code> \n\nâ² [ÙØ³ÙØ³ÙØ§Øª Ø±ÙØ¶Ø§Ù](https://t.me/RamadanTv_2023)\nâ² [Ø¬Ø±ÙØ¨ Ø§ÙØ·ÙØ¨Ø§Øª](https://t.me/RamadanTv2023)</b>")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "ð® á´Éªá´á´Êá´ : <a href={url}>{title}</a>\nð Êá´á´Ê : {year}\nð­ É¢á´É´Êá´ : {genres}\nð Êá´á´ÉªÉ´É¢ : <a href={url}/ratings>{rating} IMDB</a>\nâ° Êá´É´á´Éªá´á´ : {runtime} ð¼ðððððð\nð¹ sá´á´sá´É´s : {seasons}\nðï¸ Êá´É´É¢á´á´É¢á´ : {languages}\nð á´á´á´É´á´ÊÉªá´s : {countries}\nð sá´á´ÊÊ : {plot} \n\n  â¡ï¸Pá´á´¡á´Êá´á´ BÊ : <a href=https://t.me/TorrentSeriess><b>AÊÊá´á´¡FÊÉªx</b></a>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "False"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

