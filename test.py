import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
     ydl.download(['https://vk.com/video/@tvoy_papa_ept?z=video-134176512_456239276%2Fpl_284212489_-2'])