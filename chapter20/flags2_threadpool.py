# Example 20-16
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus
from flags2_sequential import download_one  # 1


DEFAULT_CONCUR_REQ = 30  # 2
MAX_CONCUR_REQ = 1000  # 3


def download_many(
        cc_list: list[str],
        base_url: str,
        verbose: bool,
        concur_req: int
    ) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    
    with ThreadPoolExecutor(max_workers=concur_req) as executor:  # 4
        to_do_map = {}  # 5
    
        for cc in sorted(cc_list):  # 6
            future = executor.submit(download_one, cc, base_url, verbose)  # 7
            to_do_map[future] = cc  # 8
    
    done_iter = as_completed(to_do_map)  # 9
    
    if not verbose:
        done_iter = tqdm.tqdm(done_iter, total=len(cc_list))  # 10
    
    for future in done_iter:  # 11
        try:
            status = future.result()  # 12
        except httpx.HTTPStatusError as exc:  # 13
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg.format(resp=exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''
        
        if error_msg:
            status = DownloadStatus.ERROR
        
        counter[status] += 1

        if verbose and error_msg:
            cc = to_do_map[future]  # 14
            print(f'{cc} error: {error_msg}')
    
    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)