import asyncio
import json
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.inline import button_resolutions
from main import dp
from utils.helpers import send_message
from utils.match_urls import match_urls
from utils.tiktok.tiktok_helpers import get_tik_tok_url
from utils.vk.vk_main import get_vk_video
from utils.youtube.youtube_main import get_youtube_url


@dp.callback_query_handler(text_contains='resolution_')
@dp.throttled(rate=15)  # Prevent flooding
async def chat_messages(query: types.CallbackQuery, state: FSMContext):
    lang = "ru"
    answer_data = query.data
    async with state.proxy() as data:
        t = json.loads(data["data"])
    print()
    await state.finish()
    # if answer_data.startswith("url_"):
    #     await send_message(message.chat.id, "send_video", lang, last_message.message_id)
    #
    #     if await send_video(message.chat.id, link, lang):
    #         await send_message(message.chat.id, "send_video_complete", lang, last_message.message_id)
    #     else:
    #         await asyncio.sleep(.5)
    #         await send_message(message.chat.id, "failed_send_video", lang, last_message.message_id)
    #         await send_message(message.chat.id, "send_video_link", lang, args=link)


@dp.message_handler()  # Answer to all messages
@dp.throttled(rate=2)  # Prevent flooding
async def chat_messages(message: Message):
    lang = "ru"
    last_message = await send_message(message.chat.id, "search_video", lang)
    host = await match_urls(message.text)

    if host == "TIKTOK":
        data, error = await get_tik_tok_url(message.text)
    elif host == "YOUTUBE":
        data, error = await get_youtube_url(message.text)
    elif host == "VK":
        data, error = await get_vk_video(message.text)
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
