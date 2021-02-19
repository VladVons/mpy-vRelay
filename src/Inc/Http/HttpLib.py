'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.03
License:     GNU, see LICENSE for more details
Description:.
'''

#import socket
import uasyncio as asyncio
#
from Inc.Util.UStr import SplitPad


async def CheckHost(aHost: str, aPort: int = 80, aTimeOut: int = 1) -> bool:
    try:
        await asyncio.wait_for(asyncio.open_connection(aHost, aPort), timeout=aTimeOut)
        R = True
    except:
        R = False
    return R

async def ReadHead(aReader: asyncio.StreamReader, aServ = True) -> dict:
    R = {}
    while True:
        Data = await aReader.readline()
        if (Data == b'\r\n') or (Data is None):
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