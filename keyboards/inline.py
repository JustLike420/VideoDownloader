from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import dp
from utils.helpers import send_photo, delete_message, user_msg

language = "HTML"
generate_follow_markup = ""


async def button_resolutions(chat_id, msg_str, lang, last_message_id, data):
    try:
        keyboard = InlineKeyboardMarkup()
        for info in data["resolutions"]:
            keyboard.add(
                InlineKeyboardButton(text=info["resolution"], callback_data=f"resolution_{info['resolution']}"))
        await delete_message(chat_id, last_message_id)
        caption = await user_msg(msg_str, lang, data["title"])
        last_message_id = await send_photo(chat_id, data["thumbnail_url"], caption=caption, parse_mode="HTML",
                                           disable_notification=True,
                                           reply_markup=keyboard)
        state = dp.get_current().current_state()
        await state.update_data(video_data=data["resolutions"])
        await state.update_data(user_data={
            "chat_id": chat_id,
            "last_message_id": last_message_id.message_id,
            "lang": lang,
        })
    except Exception as err:
        print('[ERROR] in button_resolutions\nException: {}\n\n'.format(err))
        return None
