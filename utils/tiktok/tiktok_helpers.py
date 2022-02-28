import copy

import aiohttp

from api.video_api import video_api
from data.config import HEADERS

VIDEO_REQUEST_URL = 'https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{}%5D'

TIKTOK_LIST = ['tiktok.com/@', 'likee.video', 'vm.tiktok.com', 'likee.com/v', 'm.tiktok.com', '.html?', 'vt.tiktok.com']


# Function to get tiktok video and audio url
async def get_tik_tok_data(link):
    async with aiohttp.ClientSession() as session:
        video_id, error = await get_tik_tok_video_id(session, link)
        if video_id is None:
            return video_id, error

        video_data, error = await get_tik_tok_video(session, video_id)
        return video_data, error


async def get_tik_tok_video_id(session, link):
    try:
        get_request = await session.get(link, headers=HEADERS, allow_redirects=True)
        redirected_url = str(get_request.url)
        if redirected_url in ['https://www.tiktok.com']:
            return None, 'wrong'

        # Check if the link is user url
        if '@' in redirected_url and all(x not in redirected_url for x in ['/video/', '/v/', '/music/']):
            return None, 'wrong'

        # Check if the link is music url
        if '/music/' in redirected_url:
            return None, 'audio-bot'

        # Get video id by redirect url
        if 'com/v/' in redirected_url:
            video_id = redirected_url.split('/v/')[1].split('.')[0].replace('/', '')
        else:
            video_id = redirected_url.split('/video/')[1].split('?')[0].replace('/', '')

        return video_id, None

    except Exception as err:
        print(err, '[ERROR] in get_tik_tok_video_id - ', link)
        return None, 'wrong'


########################################################################################################################


# Get tiktok video url without watermark
async def get_tik_tok_video(session, video_id):
    try:
        url_to_request = VIDEO_REQUEST_URL.format(video_id)
        get_request = await session.get(url_to_request)
        response_json = await get_request.json()
        api = video_api()
        if response_json is not None and 'aweme_details' in response_json.keys():
            api.thumbnail_url = response_json['aweme_details'][0]['video']['cover']['url_list'][-1]
            api.title = response_json['aweme_details'][0]['desc']
            api.author = response_json['aweme_details'][0]['author']['unique_id']
            video_info = response_json['aweme_details'][0]['video']
            if video_info['bit_rate'] and 'play_addr' in video_info['bit_rate'][0]:
                video_urls = video_info['bit_rate'][0]['play_addr']['url_list']
            else:
                video_urls = video_info['play_addr']['url_list']

            api.link = video_urls[0]
            return api, None

    except Exception as err:
        print(err, 'Error in get_tik_tok_video\n')
        return None, "non_error"


########################################################################################################################


# Function to get likee video url
async def get_like_video_url(user_link):
    async with aiohttp.ClientSession() as session:
        async with session.get(user_link, headers=HEADERS, allow_redirects=True) as get_request:
            redirect_url = str(get_request.url)
            video_id = redirect_url.split('?')[1].split('=')[1]

            data = {'postIds': video_id}
            url = 'https://likee.video/official_website/VideoApi/getVideoInfo'
            async with session.post(url, headers=HEADERS, data=data) as get_request:
                video_json = await get_request.json()
                video_list = video_json['data']['videoList']
                if not video_list:
                    return None, 'unable'
                else:
                    video_url = video_list[0]['videoUrl']

                video_no_water_url = video_url.replace('_4', '')

            return video_no_water_url, 'unable'


########################################################################################################################


# Function to download video or audio
async def download_file(link, chat_id):
    file_directory = f'video/{chat_id}.mp4'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS, timeout=30) as get_video:
                with open(file_directory, "wb") as file_stream:
                    video_url_content = await get_video.content.read()
                    file_stream.write(video_url_content)

                return file_directory

    except Exception as err:
        print(err, 'Error in download_file')
        return None


# if __name__ == '__main__':
#     asyncio.run(get_like_video_url('https://l.likee.video/v/7v9ZcX'))
