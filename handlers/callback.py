import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.all_messages import send
from keyboards.inline import link_in_button
from main import dp
from utils.helpers import send_message, delete_message, send_video, get_link_via_resolution


@dp.callback_query_handler(lambda call: call.data.startswith('resolution_'))
@dp.throttled(rate=3)  # Prevent flooding
async def chat_messages(query: types.CallbackQuery, state: FSMContext):
    try:
        await send(query, state)
    except Exception as err:
        await state.reset_state()
        print('[ERROR] in chat_messages\nException: {}\n\n'.format(err))

# # Answer to called button
# @dp.callback_query_handler()
# async def callback_message(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     call_data = str(call.data)
#
#     await call.answer()
#
#     # Update user lang
#     if any(call_data == x for x in ['ru', 'en', 'uz']):
#         await call.message.delete()
#         await send_message(chat_id, 'start', call_data)
#         users_db.set(chat_id, call_data)
