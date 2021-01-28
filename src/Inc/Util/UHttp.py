'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.03
License:     GNU, see LICENSE for more details
Description:.
'''

#import socket
import uasyncio as asyncio
#
from .UStr import SplitPad

'''
def GetMime(aExt: str) -> str:
    R = {
        'html' : 'text/html',
        'css'  : 'text/css',
        'js'   : 'text/javascript',
        'png'  : 'image/png',
        'gif'  : 'image/gif',
        'jpg'  : 'image/jpeg'
    }
    return R.get(aExt, 'text/plain')
'''

async def CheckHost(aHost: str, aPort: int = 80, aTimeOut: int = 1) -> bool:
    try:
        await asyncio.wait_for(asyncio.open_connection(aHost, aPort), timeout=aTimeOut)
        R = True
    except:
        R = False
    return R

async def ReadHead(aReader, aServ = True) -> dict:
    R = {}
    while True:
        Data = await aReader.readline()
        if (Data == b'\r\n'):
            break

        Data = Data.decode('utf-8').strip()
        if (len(R) == 0):
            if (aServ):
                R['mode'], R['url'], R['prot'] = SplitPad(3, Data, ' ')
                R['path'], R['query'] = SplitPad(2, R['url'], '?')
            else:
                R['prot'], R['code'], R['status'] = SplitPad(3, Data, ' ')
        else:
            Key, Value = SplitPad(2, Data, ':')
            R[Key.lower()] = Value.strip()
    return R

async def UrlLoad(aUrl: str, aWriter):
    _, _, Host, Path = aUrl. split('/', 3)
    Reader, Writer = await asyncio.open_connection(Host, 80)
    Data = bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (Path, Host), 'utf8')
    Writer.write(Data)
    await Writer.drain()

    Head = await ReadHead(Reader, False)
    if (Head.get('code', '404') == '200'):
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
