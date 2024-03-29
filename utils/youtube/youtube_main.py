from pytube import YouTube

from api.video_api import video_api


# from pytube import YouTube
# YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
# yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url


async def get_youtube_data(link):
    try:
        youtube = YouTube(link)
        api = video_api()
        api.thumbnail_url = youtube.thumbnail_url
        api.title = youtube.title
        api.author = youtube.author
        youtube = youtube.streams.filter(progressive=True, file_extension="mp4").desc().fmt_streams
        for data in youtube:
            api.resolutions.append(
                {
                    "resolution": data.resolution,
                    "url": data.url,
                }
            )
        return api, None
    except Exception as err:
        print('[ERROR] in button_resolutions\nException: {}\n\n'.format(err))
        return None, "failed_get_link"
