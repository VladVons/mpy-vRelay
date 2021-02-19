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
from Inc.Conf import Conf


def Test1():
    wdt = machine.WDT()

    Loops = 0
    while True:
        Loops += 1
        print('Loops', Loops)
        time.sleep(0.1)


class TClass():
    async def Test1(self):
        from Inc.Util.UNet import CheckHost
        while True:
            State = await CheckHost('8.8.8.8', 53, 2)
            if (not State):
                await self.Connect()

            print('Test1', State)
            await asyncio.sleep(5)

    async def Prove(self):
        Loops = 0
        while True:
            Loops += 1
            print('Prove', Loops)
            await asyncio.sleep(1)
 
    async def Connect(self):
        from App.Utils import TWLanApp
        if (Conf.STA_ESSID):
            WLan = TWLanApp()
            if (await WLan.TryConnect()):
                print('Connect Ok')
            else:
                print('Connect Err')

    def Run(self):
        asyncio.run(self.Connect())

        loop = asyncio.get_event_loop()
        loop.create_task(self.Prove())
        loop.create_task(self.Test1())
        loop.run_forever()

#Test1()

Class = TClass()
Class.Run()
