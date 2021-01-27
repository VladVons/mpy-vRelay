'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.03
License:     GNU, see LICENSE for more details
Description:.
'''

import socket
import uasyncio as asyncio


def CheckHostPort(aHost: str, aPort: str, aTimeOut: int = 1) -> bool:
    Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Sock.settimeout(aTimeOut)
    try:
        R = (Sock.connect_ex((aHost, aPort)) == 0)
        Sock.close()
    except:
        R = False
    return R

async def GetHttpHead(aReader) -> dict:
    R = {}

    while True:
        Line = await aReader.readline()
        if (not Line) or (Line == b'\r\n'):
            break

        Line = Line.decode("utf-8")
        Arr = Line.split(':')
        if (len(Arr) == 1):
            Key   = 'head'
            Value = Arr[0]
        else:
            Key   = Arr[0]
            Value = Arr[1]
        R[Key.lower()] = Value.strip()
    return R

async def UrlLoad(aUrl: str, aWriter):
    _, _, Host, Path = aUrl. split('/', 3)
    Reader, Writer = await asyncio.open_connection(Host, 80)
    Data = bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (Path, Host), 'utf8')
    Writer.write(Data)
    await Writer.drain()

    Head = await GetHttpHead(Reader)
    Arr  = Head.get('head', '').split(' ')
    if (len(Arr) < 2) or (Arr[1] != '200'):
        return

    Len = int(Head.get('content-length', 0))
    if (Len > 0):
        while True:
            Data = await Reader.read(512)
            if (not Data):
                break
            aWriter.write(Data)
            await asyncio.sleep(0.05)
        aWriter.flush()
    Writer.close()
    await Writer.wait_closed()
