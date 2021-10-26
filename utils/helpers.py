# coding=utf-8
from main import bot
from data.messages import msg_dict


# Function to send waiting message
async def send_message(chat_id, msg_str, lang, args=None, markup=None, parse=None, hide_preview=True):
    try:
        msg_to_send = await user_msg(msg_str, lang, args)
        sent_message = await bot.send_message(chat_id, msg_to_send, reply_markup=markup, parse_mode=parse,
                                              disable_web_page_preview=hide_preview, disable_notification=True)
        return sent_message
    except Exception as err:
        print('[ERROR] in send_message\nException: {}\n\n'.format(err))
        return None


async def get_chat_member(channel_id, chat_id):
    try:
        user_following_info = await bot.get_chat_member(channel_id, chat_id)
        return user_following_info
    except:
        return None


# Function to send a video
async def send_video(chat_id, link, lang):
    try:
        await send_message(chat_id, "download", "ru")

        await bot.send_video(chat_id, link, disable_notification=True)
        return True
    except Exception as err:
        print('[ERROR] in send_video\nException: {}\n\n'.format(err))
        await send_message(chat_id, "send_video_link", lang, link)
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

    correct_user_message = user_message.replace('_', '\_')
    return correct_user_message
