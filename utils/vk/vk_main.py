from data.config import HEADERS
from requests_html import AsyncHTMLSession
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import requests

session = AsyncHTMLSession()


async def get_vk_video(link: str):
    try:
        link = urlparse(link)
        query = parse_qs(link.query)
        if "m." not in link[1]:
            host = "m." + link[1]
        else:
            host = link[1]
        if query:
            link = f"{link[0]}://{host}/{query['z'][0]}"
        else:
            link = f"{link[0]}://{host}{link[2]}"
        response = await session.get(link, headers=HEADERS)
        await response.html.arender()
        link = response.html.find("div.VideoPage__video > video > source[type='video/mp4']", first=True).attrs['src']
        # soup = BeautifulSoup(response.html.html, "lxml")
        # link = soup.select_one("video source[type='video/mp4']").attrs["src"]
        # link = urlparse(link)
        # link = f"{link[0]}://{link[1]}{link[2]}"
        return link, None
    except Exception as err:
        return None, "failed_get_link"

    # async def get_link(link):
