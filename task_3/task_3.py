import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

import aiohttp
import requests
from tqdm import tqdm

REQUESTS_COUNTS = 1000


def do_get_request(url: str):
    try:
        resp = requests.get(url)

    except requests.exceptions.ConnectionError:
        return {"error": "ConnectionError"}

    except Exception as other_exc:
        return {"error": repr(other_exc)}

    else:
        json_data = resp.json()
        return json_data


def get_request_threading():
    url = input("Введите нужный url адрес:\n")

    with tqdm(total=REQUESTS_COUNTS) as pbar:
        with ThreadPoolExecutor(max_workers=REQUESTS_COUNTS) as ex:
            futures = [ex.submit(do_get_request, url) for _ in range(REQUESTS_COUNTS)]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)


def get_request_aiohttp():
    url = 'http://www.python.org'
    pbar = tqdm(total=REQUESTS_COUNTS)

    async def call_url(link: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                data = await resp.text()
        pbar.update(1)
        return data

    futures = [call_url(url) for _ in range(REQUESTS_COUNTS)]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))


if __name__ == '__main__':
    # 1000 запросов мультипоточно
    get_request_threading()
    # 1000 запросов асинхронно
    # get_request_aiohttp()
