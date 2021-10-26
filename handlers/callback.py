from aiogram.types import CallbackQuery

from utils.helpers import send_message
from main import dp, users_db


# Answer to called button
@dp.callback_query_handler()
async def callback_message(call: CallbackQuery):
    chat_id = call.message.chat.id
    call_data = str(call.data)

    await call.answer()

    # Update user lang
    if any(call_data == x for x in ['ru', 'en', 'uz']):
        await call.message.delete()
        await send_message(chat_id, 'start', call_data)
        users_db.set(chat_id, call_data)

