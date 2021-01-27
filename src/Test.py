#!/usr/bin/micropython
#!/usr/bin/python3


import os
import uio
import json
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log import Log
from App.Utils import TWLanApp
from Inc.Util.UNet import GetHttpHead


async def Test1():
    while True:
        print('Test1')
        await asyncio.sleep(5)


async def GetHttpHead1(aReader) -> dict:
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

    Head = await GetHttpHead1(Reader)
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
            await asyncio.sleep(0.1)
        aWriter.flush()
    Writer.close()
    await Writer.wait_closed()

async def DownloadList(aUrl: str) -> bool: 
    Buf = uio.BytesIO()
    try:
        await UrlLoad(aUrl, Buf)
        Data = Buf.getvalue().decode("utf-8")
        Data = json.loads(Data)
    except Exception as E:
        Log.Print(1, 'x', 'DownloadList()', E)
        return False

    Size = 0
    Root = aUrl.rsplit('/', 1)[0]
    Files = Data.get('Files', [])
    for File in Files:
        Arr = File.rsplit('/', 1)
        if (len(Arr) == 2):
            try:
                os.mkdir(Arr[0])
            except: pass

        Url = Root + '/' + File
        with open(File, "w") as hFile:
            await UrlLoad(Url, hFile)
            hFile.seek(0, 2)
            print('--x', Root, Url, File, Data.get('Size', 0), hFile.tell())
            Size += hFile.tell()

    return Data.get('Size', 0) == Size


async def Test2():
    Url = "http://download.oster.com.ua/www/relay/ver.json"
    R = await DownloadList(Url)
    print('---R', R)


def Stream():
    Buf = uio.StringIO()
    print('Buf', dir(Buf))


def Connect():
    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print('Net OK')


#Stream()

Connect()

loop = asyncio.get_event_loop()
#loop.create_task(Test1())
loop.create_task(Test2())
loop.run_forever()
