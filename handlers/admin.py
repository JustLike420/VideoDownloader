# coding=utf-8
from aiogram.types import Message

from admin.get_saved_ads import get_saved_ads_func, save_add_func
from admin.get_users_by_lang import get_users_by_lang_func
from admin.necessary_following import add_necessary_following_func
from main import ADMIN_ID, dp, ADMIN_LIST_COMMANDS, bot
from keyboards.buttons import admin_buttons, text_ad_markup
from admin.get_bot_stat import get_bot_stat_func
from admin.send_everyone import send_everyone_func
from admin.backup_users_id import backup_users_id_func


# Answer to /admin command
@dp.message_handler(lambda message: message.chat.id == int(ADMIN_ID) and message.text in ADMIN_LIST_COMMANDS)
async def admin_commands(message: Message):
    admin_command = message.text

    if admin_command == 'Рассылка рекламы':
        await send_everyone_func()

    elif admin_command == 'Бекап базы':
        await backup_users_id_func()

    elif admin_command == 'Обязательная подписка':
        await add_necessary_following_func()

    elif admin_command == 'Статистика бота':
        await get_bot_stat_func()

    elif admin_command == 'Пользователи по языкам':
        await get_users_by_lang_func()

    elif admin_command == 'Статистика рекламы':
        await get_saved_ads_func()

    elif admin_command == 'Сохранить рекламу':
        await save_add_func()

    elif admin_command == 'Рекламные показы':
        await bot.send_message(ADMIN_ID, 'Возможные действия для рекламнных показов по кнопкам ниже',
                               reply_markup=text_ad_markup)

    elif admin_command == '/admin':
        await bot.send_message(ADMIN_ID, 'Все команды админа', reply_markup=admin_buttons)


