import os

from keyboards.inline import generate_follow_markup

from utils.tiktok.tiktok_helpers import download_file, get_like_video_url, TIKTOK_LIST
from utils.help_functions import update_statistics, check_user_info, check_ad, admin_channel_to_follow
from utils.helpers import send_message, send_video, get_chat_member


async def tik_tok_main_func(chat_id, user_link):
    user_lang = await check_user_info(chat_id)
    if not user_lang:
        return

    channel_link = admin_channel_to_follow['link']
    channel_id = admin_channel_to_follow['id']

    if user_lang == 'ru' and channel_link:
        user_info = await get_chat_member(channel_id, chat_id)
        if user_info is not None:
            if user_info['status'] != 'member':
                follow_markup = await generate_follow_markup(channel_link)
                await send_message(chat_id, 'follow', user_lang, markup=follow_markup)
                return

    # Check if the user message is link
    if any(x in user_link for x in TIKTOK_LIST) and all(x not in user_link for x in [' ', '\n']):
        sent_message = await send_message(chat_id, 'wait', user_lang)
        await send_to_chat_by_link(chat_id, user_link, user_lang)
        await sent_message.delete()
    else:
        await send_message(chat_id, 'wrong', user_lang)


# Function to send video and audio by link
async def send_to_chat_by_link(chat_id, user_link, user_lang):
    user_link = 'http{}'.format(user_link.split('http')[1])

    # Check if the url is from Likee or TikTok
    if 'tiktok' in user_link:
        video_url, error_type = await get_tik_tok_url(user_link)
    else:
        video_url, error_type = await get_like_video_url(user_link)

    # Check if both urls are None
    if video_url is None:
        await send_message(chat_id, error_type, user_lang)
        if error_type == 'unable':
            await update_statistics('error')
        return

    # Update statistics
    await update_statistics('download')

    is_sent = await send_video(chat_id, video_url, user_lang, user_link)
    if not is_sent:
        file_dir = await download_file(video_url, chat_id)
        is_sent = await send_video(chat_id, open(file_dir, 'rb'), user_lang, user_link)
        os.remove(file_dir)

    if 'like.video' in video_url and not is_sent:
        await send_message(chat_id, 'like-video', user_lang, args=video_url, parse='markdown', hide_preview=False)
        return

    if not is_sent and '-' not in str(chat_id):
        await send_message(chat_id, 'unable', user_lang)
        return

    # Check advertisement
    if is_sent and '-' not in str(chat_id):
        await check_ad(chat_id)
