#!/usr/bin/micropython
#!/usr/bin/python3


import os
import sys
import uio
import json
import time
import select
import uasyncio as asyncio
#
#from Inc.Conf import Conf
from Inc.Log import Log
from Inc.Util import UFS

#from App.Utils import TWLanApp
#from Inc.Plugin import TPlugin

def Test1():
    poller = select.poll()
    poller.register(sys.stdin, select.POLLIN)
    while True:
        events = poller.poll()
        if (events):
            char = sys.stdin.read(1)
            print('char', char, ord(char))
        #for Arr in poll.poll(5):
            #print('Test1', Arr)
            #poll.modify(sys.stdin, select.POLLIN)
        #time.sleep(1)

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

