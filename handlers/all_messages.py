import asyncio

from aiogram.types import Message

from main import dp
from utils.helpers import send_video, send_message
from utils.match_urls import match_urls
from utils.tiktok.tiktok_helpers import get_tik_tok_url
from utils.vk.vk_main import get_vk_video
from utils.youtube.youtube_main import get_youtube_url


@dp.message_handler()  # Answer to all messages
@dp.throttled(rate=2)  # Prevent flooding
async def chat_messages(message: Message):
    lang = "ru"
    last_message = await send_message(message.chat.id, "search_video", "ru")
    host = await match_urls(message.text)

    if host == "TIKTOK":
        link, error = await get_tik_tok_url(message.text)
    elif host == "YOUTUBE":
        link, error = await get_youtube_url(message.text)
    elif host == "VK":
        link, error = await get_vk_video(message.text)
    else:
        await send_message(message.chat.id, "url_not_match", lang, last_message.message_id)
        return
    if error is not None:
        await send_message(message.chat.id, error, lang, last_message.message_id)
        return
    print(link)
    await send_message(message.chat.id, "search_complete", lang, last_message.message_id)
    await asyncio.sleep(1)
    await send_message(message.chat.id, "send_video", lang, last_message.message_id)

    if await send_video(message.chat.id, link, lang):
        await send_message(message.chat.id, "send_video_complete", lang, last_message.message_id)
    else:
        await asyncio.sleep(.5)
        await send_message(message.chat.id, "failed_send_video", lang, last_message.message_id)
        await send_message(message.chat.id, "send_video_link", lang, args=link)
