from urllib.parse import urlparse, parse_qs

from requests_html import AsyncHTMLSession

from api.video_api import video_api
from data.config import HEADERS

session = AsyncHTMLSession()


async def get_vk_data(link: str):
    try:
        parse_link = urlparse(link)
        query = parse_qs(parse_link.query)
        link = f"{parse_link[0]}://m.vk.com"
        if query:
            link += f"/{query['z'][0]}"
        else:
            link += f"{parse_link[2]}"

        response = await session.get(link, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        })
        await response.html.arender(timeout=100)
        links = response.html.find("source[type='video/mp4']")
        if not links:
            raise Exception("Link not found.")
        api = video_api()

        api.thumbnail_url = response.html.find("div.VideoPage__video > video", first=True).attrs["poster"]
        api.title = response.html.find("div.VideoPageInfoRow > h2", first=True).text
        api.author = response.html.find("a > div.Cell__main > div.Cell__title", first=True).text
        for link in links:
            url = link.attrs['src']
            if urlparse(link.attrs['src']).path != "/":
                resolution = urlparse(link.attrs['src']).path.split(".")[1]
                api.resolutions.append({
                    "resolution": resolution,
                    "url": url,
                })
            else:
                api.link = url
                break

                # soup = BeautifulSoup(response.html.html, "lxml")
        # link = soup.select_one("video source[type='video/mp4']").attrs["src"]
        # link = urlparse(link)
        # link = f"{link[0]}://{link[1]}{link[2]}"
        return api, None
    except Exception as err:
        print('[ERROR] in get_vk_data\nException: {}\n\n'.format(err))
        return None, "failed_get_link"

    # async def get_link(link):
