from aiogram import types
from main import dp, bot
from utils.helpers import send_message


@dp.message_handler(commands=["start"])
async def say_hello(message: types.Message):
    lang = "ru"
    await send_message(message.chat.id, "start", lang)
