from pytube import YouTube


# from pytube import YouTube
# YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
# yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url


async def get_youtube_url(link):
    try:
        link = YouTube(link).streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().url
        return link, None
    except:
        return None, "failed_get_link"
