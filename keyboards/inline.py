from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import dp
from utils.helpers import send_photo, delete_message, user_msg
from api.video_api import video_api

language = "HTML"
generate_follow_markup = ""


async def link_in_button(link):
    keyboard = InlineKeyboardMarkup()
    return keyboard.add(InlineKeyboardButton('Скачать', url=link))


async def button_resolutions(chat_id, msg_str, lang, last_message_id, data: video_api):
    try:
        keyboard = InlineKeyboardMarkup()
        for info in data.resolutions:
            keyboard.add(
                InlineKeyboardButton(text=info["resolution"], callback_data=f"resolution_{info['resolution']}"))
        await delete_message(chat_id, last_message_id)
        caption = await user_msg(msg_str, lang, (data.author, data.title))
        state = dp.get_current().current_state()

        if data.resolutions:
            last_message_id = await send_photo(chat_id, data.thumbnail_url, caption=caption, parse_mode="HTML",
                                               disable_notification=True,
                                               reply_markup=keyboard)
            await state.update_data(video_data=data.resolutions)
            await state.update_data(user_data={
                "last_message_id": last_message_id.message_id if last_message_id is not None else None,
                "lang": lang,
            })
            return False
        else:
            await state.update_data(video_data=data.link)
            await state.update_data(user_data={
                "last_message_id": None,
                "lang": lang,
            })
            return True

    except Exception as err:
        print('[ERROR] in button_resolutions\nException: {}\n\n'.format(err))
        return False


btnUrlChannel = InlineKeyboardButton(text='КАНАЛ #1 ➡', url='https://t.me/IT_wworld')
btnDoneSub = InlineKeyboardButton(text='✅ Я подписался', callback_data="sub_channeldone")
checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(btnUrlChannel)
checkSubMenu.insert(btnDoneSub)
