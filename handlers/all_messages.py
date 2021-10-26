from aiogram.types import Message
from main import bot
from main import dp
from utils.match_urls import match_urls
from utils.tiktok.tiktok_helpers import get_tik_tok_url
from utils.youtube.youtube_main import get_youtube_url
from utils.vk.vk_main import get_vk_video
from utils.helpers import send_video, send_message


@dp.message_handler()  # Answer to all messages
@dp.throttled(rate=2)  # Prevent flooding
async def chat_messages(message: Message):
    await send_message(message.chat.id, "search_video", "ru")
    host = await match_urls(message.text)

    if host == "TIKTOK":
        url, error = await get_tik_tok_url(message.text)
    elif host == "YOUTUBE":
        url, error = await get_youtube_url(message.text)
    elif host == "VK":
        url, error = await get_vk_video(message.text)
    else:
        await send_message(message.chat.id, "url_not_match", "ru")
        return
    if error is not None:
        await send_message(message.chat.id, error, "ru")
        return
    await send_message(message.chat.id, "search_complete", "ru")
    await send_video(message.chat.id, url, "ru")
