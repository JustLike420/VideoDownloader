from urllib.parse import urlparse


async def match_urls(link):
    domain = urlparse(link).netloc
    if "tiktok" in domain:
        return "TIKTOK"
    if "vk" in domain:
        return "VK"
    if "youtube" in domain or "youtu.be" in domain:
        return "YOUTUBE"
