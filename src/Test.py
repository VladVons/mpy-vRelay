#!/usr/bin/micropython
#!/usr/bin/python3


import os
import sys
import uio
import json
import uasyncio as asyncio
#
#from Inc.Conf import Conf
#from Inc.Log import Log
#from App.Utils import TWLanApp
#from Inc.Util.UHttp import GetHttpHead


async def Test1():
    while True:
        print('Test1')
        await asyncio.sleep(5)


def Print(aLevel: int, aType: str, *aParam) -> str:
    print('---x')
    sys.print_exception(aParam[1])
    #print(aLevel, aType, aParam[1], type(aParam[1]).__name__)
    print('Type1', type(aParam[1]), dir(aParam[1]))
    print('Type2', type(aParam[1]), dir(1))
    print('Type3', type(aParam[1]), dir('1'))

async def Test2():
    Url = "http://download.oster.com.ua/www/relay/ver.json"
    #$print('---R', R)
    try:
        q = 1/0
    except Exception as E:
        Print(1, 'x', 'test()', E)


def Connect():
    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print('Net OK')


#Stream()

#Connect()

loop = asyncio.get_event_loop()
#loop.create_task(Test1())
loop.create_task(Test2())
loop.run_forever()
