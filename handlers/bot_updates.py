from aiogram.types import Update

from main import dp, users_db


@dp.my_chat_member_handler()
async def catch_deleted_users(update: Update):
    chat_id = update.chat.id
    user_status = update.new_chat_member.status

    if user_status == 'kicked' and '-' not in str(chat_id):
        users_db.set(chat_id, 'None')

