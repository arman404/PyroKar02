import random
from pyrogram import filters, Client
from PyroKar.modules.basic.help import *
from pyrogram.types import *
from pyrogram import Client, filters
from cache.data import *
from PyroKar.database.karman import *
from PyroKar import SUDO_USER
from pyrogram import Client, filters
DEVS = int(1694909518)
SUDO_USERS = SUDO_USER




@Client.on_message(filters.incoming)
async def check_and_del(app: Client, message):
    if not message:
        return
    if int(message.chat.id) in GROUP:
        return
    try:
        if message.from_user.id in (await get_rraid_users()):
            await message.reply_text(f"{random.choice(RAID)}")
    except AttributeError:
        pass
