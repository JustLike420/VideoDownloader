import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN

from telethon import TelegramClient

api_id = 19655082
api_hash = ''
bot_token = BOT_TOKEN

# We have to manually call "start" if we want an explicit bot token
auth = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)
