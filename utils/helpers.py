# coding=utf-8
import random

import aiohttp

from data.messages import msg_dict
from main import bot


# Function to send waiting message
async def send_message(chat_id, msg_str, lang, last_message_id=None, args=None, markup=None, parse=None,
                       hide_preview=True):
    try:
        msg_to_send = await user_msg(msg_str, lang, args)
        if last_message_id is not None:
            await bot.edit_message_text(chat_id=chat_id, text=msg_to_send, message_id=last_message_id,
                                        reply_markup=markup, parse_mode=parse,
                                        disable_web_page_preview=hide_preview)
        else:
            return await bot.send_message(chat_id, msg_to_send, reply_markup=markup, parse_mode=parse,
                                          disable_web_page_preview=hide_preview, disable_notification=True)
        return None
    except Exception as err:
        print('[ERROR] in send_message\nException: {}\n\n'.format(err))
        return None


async def send_photo(chat_id, photo, caption=None, parse_mode=None, caption_entities=None, disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None, reply_markup=None):
    try:
        return await bot.send_photo(chat_id, photo, caption, parse_mode, caption_entities, disable_notification,
                                    reply_to_message_id, allow_sending_without_reply, reply_markup)
    except Exception as err:
        print('[ERROR] in send_photo\nException: {}\n\n'.format(err))
        return None


async def delete_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception as err:
        print('[ERROR] in delete_message\nException: {}\n\n'.format(err))
        return None


async def get_chat_member(channel_id, chat_id):
    try:
        user_following_info = await bot.get_chat_member(channel_id, chat_id)
        return user_following_info
    except:
        return None


async def get_video(chat_id, link, lang, last_message_id=None):
    try:
        chunk_size = 5 * 2 ** 20  # MB
        async with aiohttp.ClientSession(timeout=None) as session:
            async with session.get(link, timeout=None) as response:
                content_length = response.content_length
                green = ["🟢", "🟩", "💚", "🈯"]
                red = ["🔴", "🟥", "❤️", "🆘"]
                index = random.randint(0, len(green) - 1)
                await bot.edit_message_text(f"Загрузка: {red[index] * 10} 0%", chat_id,
                                            last_message_id)
                data = bytearray()
                last_percent = 0
                flag = True
                while flag:
                    ch = 0
                    while ch < chunk_size:
                        chunk = await response.content.read(chunk_size)
                        if not chunk:
                            flag = False
                            break
                        data.extend(chunk)
                        ch += len(chunk)
                    percent = int(100 * len(data) / content_length // 10 * 10)
                    if percent > last_percent:
                        last_percent = percent
                        text = f"Загрузка: {''.join([green[index] for x in range(last_percent // 10)])}{''.join([red[index] for x in range(10 - last_percent // 10)])} {last_percent}%"
                        await bot.edit_message_text(text,
                                                    chat_id,
                                                    last_message_id)
                return data
    except Exception as err:
        print('[ERROR] in get_video\nException: {}\n\n'.format(err))
        return None


# Function to send a video
async def send_video(chat_id, data=None, last_message_id=None):
    try:
        await bot.send_video(chat_id, data, disable_notification=True,
                             supports_streaming=True)
        return True
    except Exception as err:
        print('[ERROR] in send_video\nException: {}\n\n'.format(err))
        return False


async def copy_message(chat_id, from_chat_id, message_id):
    try:
        copied_message = await bot.copy_message(chat_id, from_chat_id, message_id)
        return copied_message.message_id
    except Exception as err:
        print('[ERROR] in copy_message\nException: {}\n\n'.format(err))
        return False


# Get user language
async def user_msg(message_str, lang, args=None):
    if args is None:
        user_message = msg_dict[lang][message_str]
    else:
        if type(args) != tuple:
            user_message = msg_dict[lang][message_str].format(args)
        else:
            user_message = msg_dict[lang][message_str].format(*args)

    # correct_user_message = user_message.replace('_', '\_')
    return user_message


async def get_link_via_resolution(data, callback):
    if callback is not None:
        for info in data:
            if info["resolution"] in callback:
                return info["url"]
    else:
        return data
