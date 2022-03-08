# video_api = {
#     "thumbnail_url": "",
#     "title": "",
#     "author": "",
#     "link": "",  # если нет выбора качества видео
#     "resolutions": [],
# }


class video_api(object):
    def __init__(self):
        self.thumbnail_url = ""
        self.title = ""
        self.author = ""
        self.link = ""  # если нет выбора качества видео
        self.resolutions = []
