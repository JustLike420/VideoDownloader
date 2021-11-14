from aiogram.types import Message

from main import dp, bot
from keyboards.inline import language, checkSubMenu
from utils.helpers import send_message, check_sub_channel
from utils.help_functions import check_user_info

CHANNEL_ID = "@IT_wworld"


# Answer to all bot commands
@dp.message_handler(commands=['start'])
async def bot_commands(message: Message):
    # user_message = str(message.text).split()[0].replace('/', '').lower()
    # if user_message == 'lang':
    #     await send_message(message.chat.id, 'lang', 'ru', markup=language)
    #     return
    #
    # user_lang = await check_user_info(message.chat.id)
    # if user_lang:
    #     await send_message(message.chat.id, user_message, user_lang, parse='markdown')
    text = f'Привет *{message.from_user.first_name}*, отправь мне ссылку на видео из TikTok / Youtube / VK и я скачаю ' \
           f'его без водяного знака \n\n 🤟 Приятного использования! '
    await bot.send_message(message.chat.id, text, parse_mode="Markdown")


@dp.callback_query_handler(text='sub_channeldone')
async def subchanneldone(message: Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, 'Привет!')
    else:
        # await bot.answer_callback_query(callback_query.id, text='Оплата не найдена')
        await bot.send_message(message.from_user.id,
                               'Наш бот на 100% БЕСПЛАТНЫЙ и не имеет рекламы. Но доступ предоставляется только подписчикам спонсорского канала:\n'
                               '1. 👉 В мире IT (https://t.me/IT_wworld)\n\n'
                               'Присоединитесь к каналу, а затем нажмите кнопку «Я подписался». Тогда доступ будет предоставлен автоматически.',
                               reply_markup=checkSubMenu)
