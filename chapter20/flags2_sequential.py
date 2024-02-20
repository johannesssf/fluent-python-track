# flags2_sequential.py

from collections import Counter
from http import HTTPStatus

import httpx
import tqdm  # 1

from flags2_common import main, save_flag, DownloadStatus  # 2

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


def get_flag(base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()  # 3
    return resp.content


def download_one(cc: str, base_url: str, verbose: bool = False) -> DownloadStatus:
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc:  #4
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:  # 5
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise  # 6
    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'
    
    if verbose:  # 7
        print(cc, msg)
    
    return status


def download_many(cc_list: list[str], base_url: str, verbose: bool, _unused_concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()  # 1
    cc_iter = sorted(cc_list)  # 2
    
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)  # 3
    
    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose)  # 4
        except httpx.HTTPStatusError as exc:  # 5
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        except httpx.ReadError as exc:  # 6
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:  # 7
            break
        else:  # 8
            error_msg = ''
        
        if error_msg:
            status = DownloadStatus.ERROR  # 9
        counter[status] += 1  # 10

        if verbose and error_msg:  # 11
            print(f'{cc} error: {error_msg}')

    return counter  # 12


if __name__ == '__main__':
    main(download_many, 1, 1)