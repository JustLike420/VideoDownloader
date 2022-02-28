import aiohttp
import asyncio
import time

start_time = time.time()


async def main():
    async with aiohttp.ClientSession() as session:
        pokemon_url = f'https://vm.tiktok.com/ZSeRyktva/'
        async with session.get(pokemon_url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
            }) as resp:
            pokemon = await resp.text()
            print(pokemon)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print("--- %s seconds ---" % (time.time() - start_time))
