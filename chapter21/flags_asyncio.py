# Example 21-2/3
import asyncio

from httpx import AsyncClient  # 3.1

from flags import BASE_URL, save_flag, main  # 3.2


async def download_one(client: AsyncClient, cc: str):  # 3.3
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc


async def get_flag(client: AsyncClient, cc: str) -> bytes:  # 3.4
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True)  # 3.5
    return resp.read()  # 3.6


def download_many(cc_list: list[str]) -> int:  # 2.1
    return asyncio.run(supervisor(cc_list))  # 2.2


async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:  # 2.3
        to_do = [download_one(client, cc) for cc in sorted(cc_list)]  # 2.4
        res = await asyncio.gather(*to_do)  # 2.5
    
    return len(res)  # 2.6


if __name__ == '__main__':
    main(download_many)