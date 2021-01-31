#!/usr/bin/micropython
#!/usr/bin/python3


import os
import sys
import uio
import json
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log import Log
from App.Utils import TWLanApp
from Inc.Plugin import TPlugin


def TestCB():
    print('TestCB')


async def Test1():
    while True:
        print('Test1')
        await asyncio.sleep(1)


async def Test2():
    Plugin = TPlugin()
    Plugin.LoadDir('App')
    Plugin.LoadDir('Plugin/App')


def Connect():
    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print('Net OK')


#Stream()

Connect()

#asyncio.run(Test1())
#print('---x1')

asyncio.run(Test2())
#loop = asyncio.get_event_loop()
#loop.create_task(Test1())
#loop.create_task(Test2())
#loop.run_forever()
