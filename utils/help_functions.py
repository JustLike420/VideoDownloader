from datetime import date, timedelta, datetime
import json
import asyncio
from functools import wraps, partial
from data.config import *

from keyboards.inline import language
from utils.helpers import send_message, copy_message

current_month = datetime.now().strftime("%B")
current_date = str(date.today())
advertisement = {}
admin_channel_to_follow = {'link': None, 'id': None}


async def update_statistics(action):
    ...
    # global current_date
    # global advertisement
    #
    # today_date = str(date.today())
    #
    # action_db = f'{today_date}_{action}'
    # total_action_db = stats_db.get(action_db)
    # if total_action_db is None:
    #     stats_db.set(action_db, 0)
    #     total_action_db = 0
    #
    # if current_date != today_date:
    #     await update_current_month_stat()
    #     current_date = str(today_date)
    #     await send_day_statistics()
    #
    #     # Check if there is a new advertisement
    #     ad_info_db = stats_db.get(f'{current_date}_ADVERTISEMENT')
    #     if ad_info_db:
    #         advertisement = json.loads(ad_info_db)
    #     else:
    #         advertisement = {}
    #
    # total_action = int(total_action_db) + 1
    # stats_db.set(action_db, total_action)

#
# async def update_current_month_stat():
#     global current_month
#
#     total_month_db = stats_db.get(current_month)
#     if total_month_db is None:
#         stats_db.set(current_month, 0)
#         total_month_db = 0
#
#     # Get one day downloads
#     downloads = stats_db.get(f'{current_date}_download')
#     month_downloads = int(total_month_db) + downloads
#     stats_db.set(current_month, month_downloads)
#
#     today_month = str(datetime.now().strftime("%B"))
#
#     if today_month != current_month:
#         active_users = month_stat.dbsize()
#         args = current_month, int(active_users), int(total_month_db)
#         await send_message(ADMIN_ID, 'statistics', 'ru', args=args, parse='markdown')
#
#         month_stat.flushdb(asynchronous=True)
#
#         current_month = today_month
#
#
# async def send_day_statistics():
#     today_date = date.today()
#     yesterday_date = str(today_date - timedelta(days=1))
#
#     # Get one day new users
#     new_users = stats_db.get(f'{yesterday_date}_new')
#     if new_users is None:
#         new_users = 0
#
#     # Get one day downloads
#     downloads = stats_db.get(f'{yesterday_date}_download')
#     if downloads is None:
#         downloads = 0
#
#     # Get one day downloads
#     errors = stats_db.get(f'{yesterday_date}_error')
#     if errors is None:
#         errors = 0
#
#     active_users = int(files_id.dbsize())
#     if advertisement:
#         args = active_users, advertisement['message_id']
#         await send_message(ADMIN_ID, 'advertisement', 'ru', args=args, parse='markdown')
#         stats_db.delete(f'{yesterday_date}_ADVERTISEMENT')
#
#     # Send day statistics
#     args = yesterday_date, int(new_users), active_users, int(downloads), int(errors)
#     await send_message(ADMIN_ID, 'statistics', 'ru', args=args, parse='markdown')
#
#     # Update statistics
#     statistics_db = stats_db.get('STATISTICS')
#     statistics = json.loads(statistics_db)
#     statistics['downloads'] += int(downloads)
#     statistics['errors'] += int(errors)
#     stats_db.set('STATISTICS', json.dumps(statistics))
#
#     files_id.flushdb(asynchronous=True)


# Send notification that bot started working
async def on_startup(args):
    for ID in ADMIN_IDS:
        await send_message(ID, 'admin_bot_start', 'ru')
    # await update_advertisement()


async def check_ad(chat_id):
    ...
    # if advertisement and not files_id.exists(chat_id):
    #     message_id = advertisement['message_id']
    #     await copy_message(chat_id, AD_CHANNEL_ID, message_id)
    # files_id.set(chat_id, '')
    # month_stat.set(chat_id, '')


async def check_user_info(chat_id):
    if '-' in str(chat_id):
        return 'ru'

    # # If the user exists in DB, return its language
    # user_lang_db = users_db.get(chat_id)
    # if user_lang_db is not None and str(user_lang_db, 'utf-8') != 'None':
    #     return str(user_lang_db, 'utf-8')
    # else:
    #     await update_statistics('new')
    #     await send_message(chat_id, 'lang', 'ru', markup=language)
    #     users_db.set(chat_id, 'ru')

#
# def wrap(func):
#     @wraps(func)
#     async def run(*args, loop=None, executor=None, **kwargs):
#         if loop is None:
#             loop = asyncio.get_event_loop()
#         pfunc = partial(func, *args, **kwargs)
#         return await loop.run_in_executor(executor, pfunc)
#
#     return run
#
#
# async def update_advertisement():
#     global advertisement
#
#     ad_info_db = stats_db.get(f'{current_date}_ADVERTISEMENT')
#     if ad_info_db:
#         advertisement = json.loads(ad_info_db)
#
#
# async def update_channel_to_follow(channel_link, channel_id):
#     global admin_channel_to_follow
#     admin_channel_to_follow['link'] = channel_link
#     admin_channel_to_follow['id'] = channel_id
