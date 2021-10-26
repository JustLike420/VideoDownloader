from aiogram.types import Message

from main import dp
from keyboards.inline import language
from utils.helpers import send_message
from utils.help_functions import check_user_info


# Answer to all bot commands
@dp.message_handler(commands=['start', 'help', 'lang'])
async def bot_commands(message: Message):
    user_message = str(message.text).split()[0].replace('/', '').lower()
    if user_message == 'lang':
        await send_message(message.chat.id, 'lang', 'ru', markup=language)
        return

    user_lang = await check_user_info(message.chat.id)
    if user_lang:
        await send_message(message.chat.id, user_message, user_lang, parse='markdown')
