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
from Inc.KbdTerm import TKbdTerm

#from App.Utils import TWLanApp
#from Inc.Plugin import TPlugin


def Test1():
    wdt = machine.WDT()
    Cnt = 0
    while True:
        print('Cnt', Cnt)
        time.sleep(0.1)
        Cnt += 1


def Connect():
    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print('Net OK')



class TClass():
    async def ATest1(self):
        while True:
            print('ATest1')
            await asyncio.sleep(1)

    async def ATest2(self):
        KbdTerm = TKbdTerm()
        while True:
            C = KbdTerm.GetChr()
            if (C):
                print('C', C)
            await asyncio.sleep(0.1)


    def Run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.ATest1())
        loop.create_task(self.ATest2())
        loop.run_forever()

#Test1()
#Connect()

#Class = TClass()
#Class.Run()


#Minute  Hour    DOM     Month   DOW
#from Inc.Cron import IsNow
#print(IsNow('38-40 * * * *'))

Dict1 = {}
Dict1['One'] = 1
Dict1['Two'] = 2
Val = 'xxx'
for Key in Dict1.values():
    print(Key, Val)

