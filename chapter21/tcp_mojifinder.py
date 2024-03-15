# Example 21-12/14/15

import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast

from charindex import InvertedIndex, format_results  # 14.1


CRLF = b'\r\n'
PROMPT = b'?> '


async def search(query: str,  # 15.1
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    chars = index.search(query)  # 15.2
    lines = (line.encode() + CRLF for line in format_results(chars))  # 15.3
    writer.writelines(lines)  # 15.4
    await writer.drain()  # 15.5
    status_line = f'{"--" * 66} {len(chars)} found'  # 15.6
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)


async def finder(index: InvertedIndex,  # 14.2
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    client = writer.get_extra_info('peername')  # 14.3
    while True:  # 14.4
        writer.write(PROMPT)  # can't await! # 14.5
        await writer.drain()  # must await! # 14.6
        data = await reader.readline()  # 14.7
        
        if not data:  # 14.8
            break

        try:
            query = data.decode().strip()  # 14.9
        except UnicodeDecodeError:  # 14.10
            query = '\x00'
        
        print(f' From {client}: {query!r}')  # 14.11

        if query:
            if ord(query[:1]) < 32:  # 14.12
                break
            results = await search(query, index, writer)  # 14.13
            print(f'    To {client}: {results} results.')  # 14.14
    
    writer.close()  # 14.15
    await writer.wait_closed()  # 14.16
    print(f'Close {client}.')  # 14.17


async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server(  # 12.1
        functools.partial(finder, index),  # 12.2
        host, port)  # 12.3
    
    socket_list = cast(tuple[TransportSocket, ...], server.sockets)  # 12.4
    addr = socket_list[0].getsockname()
    print(f'Serving on {addr}. Hit CTRL-C to stop.')  # 12.5
    await server.serve_forever()  # 12.6


def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Building index.')
    index = InvertedIndex()  # 12.7

    try:
        asyncio.run(supervisor(index, host, port))  # 12.8
    except KeyboardInterrupt:
        print('\nServer shut down')


if __name__ == '__main__':
    main(*sys.argv[1:])