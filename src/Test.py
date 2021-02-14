#!/usr/bin/micropython
#!/usr/bin/python3


import os
import sys
import uio
import json
import time
import select
import machine
import uasyncio as asyncio
#
#from Inc.Conf import Conf
from Inc.Log import Log
from Inc.Util import UFS

#from App.Utils import TWLanApp
#from Inc.Plugin import TPlugin

def Test1():
    wdt = machine.WDT()
    Cnt = 0
    while True:
        print('Cnt', Cnt)
        time.sleep(0.1)
        Cnt += 1


async def ATest1():
    while True:
        print('ATest1')
        await asyncio.sleep(1)

async def ATest2():
    pass

def Connect():
    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print('Net OK')


Test1()
#Connect()

#asyncio.run(Test1())
#print('---x1')

#asyncio.run(ATest1())
#loop = asyncio.get_event_loop()
#loop.create_task(ATest1())
#loop.create_task(ATest2())
#loop.run_forever()

