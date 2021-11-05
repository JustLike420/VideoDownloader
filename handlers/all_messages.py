import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.inline import button_resolutions, link_in_button
from main import dp
from utils.helpers import send_message, send_video, delete_message, get_link_via_resolution
from utils.match_urls import match_urls
from utils.tiktok.tiktok_helpers import get_tik_tok_data
from utils.vk.vk_main import get_vk_data
from utils.youtube.youtube_main import get_youtube_data


@dp.callback_query_handler(lambda call: call.data.startswith('resolution_'))
@dp.throttled(rate=3)  # Prevent flooding
async def chat_messages(query: types.CallbackQuery, state: FSMContext):
    try:
        if await state.get_data():
            async with state.proxy() as data:
                link = await get_link_via_resolution(data["video_data"], query.data)
                user = data["user_data"]
            lang = user["lang"]
            chat_id = user["chat_id"]
            last_message_id = user["last_message_id"]
            await state.reset_state()
            await delete_message(chat_id, last_message_id)
            last_message_id = await send_message(chat_id, "send_video", lang)

            if await send_video(chat_id, link, lang):
                await send_message(user["chat_id"], "send_video_complete", lang, last_message_id.message_id)
            else:
                await asyncio.sleep(.5)
                await send_message(chat_id, "failed_send_video", lang, last_message_id.message_id,
                                   markup=await link_in_button(link))
    except Exception as err:
        await state.reset_state()
        print('[ERROR] in chat_messages\nException: {}\n\n'.format(err))


@dp.message_handler()  # Answer to all messages
@dp.throttled(rate=2)  # Prevent flooding
async def chat_messages(message: Message):
    lang = "ru"
    last_message = await send_message(message.chat.id, "search_video", lang)
    host = await match_urls(message.text)

    if host == "TIKTOK":
        data, error = await get_tik_tok_data(message.text)
    elif host == "YOUTUBE":
        data, error = await get_youtube_data(message.text)
    elif host == "VK":
        data, error = await get_vk_data(message.text)
    else:
        await send_message(message.chat.id, "url_not_match", lang, last_message.message_id)
        return
    if error is not None:
        await send_message(message.chat.id, error, lang, last_message.message_id)
        return
    # print(link)
    await send_message(message.chat.id, "search_complete", lang, last_message.message_id)
    await asyncio.sleep(1)
    await button_resolutions(message.chat.id, "video_preview", lang, last_message.message_id, data)
