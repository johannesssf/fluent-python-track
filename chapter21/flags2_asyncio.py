# Example 21-6/7

import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus, save_flag


# low concurrency default to avoit errors from remote site,
# such as 503 - Service Temporary Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:  # 6.1
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)  # 6.2
    resp.raise_for_status()
    return resp.content


async def download_one(client: httpx.AsyncClient, cc: str, base_url: str, semaphore: asyncio.Semaphore, verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:  #  6.3
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as exc:  # 6.4
        res = exc.response
    
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')  # 6.5
        status = DownloadStatus.OK
        msg = 'OK'
    
    if verbose and msg:
        print(cc, msg)
    
    return status


async def supervisor(cc_list: list[str], base_url: str, verbose: bool, concur_req: int) -> Counter[DownloadStatus]:  # 7.1
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)  # 7.2
    
    async with httpx.AsyncClient() as client:
        to_do = [download_one(client, cc, base_url, semaphore, verbose) for cc in cc_list]  # 7.3
        to_do_iter = asyncio.as_completed(to_do)  # 7.4
        
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # 7.5
        
        error: httpx.HTTPError | None = None  # 7.6

        for coro in to_do_iter:  # 7.7
            try:
                status = await coro
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                error = exc  # 7.9
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc  # 7.10
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR  # 7.11
                if verbose:
                    url = str(error.request.url)  # 7.12
                    cc = Path(url).stem.upper()  # 7.13
                    print(f'{cc} error: {error_msg}')
            counter[status] += 1
    
    return counter


def download_many(cc_list: list[str], base_url: str, verbose: bool, concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)  # 7.14

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)