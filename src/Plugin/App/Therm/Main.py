'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description:
'''


import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.Log  import Log
from Inc.Hyster import THyster
from Inc.DevSens import TDevSens
#
from IncP.Dev.dht22 import DHT22
from IncP.Dev.emu_cycle import TCycle


class TDevDT(TDevSens):
    def __init__(self, aPin):
        super().__init__(0.5, 10)
        #self.Dev = DHT22(aPin)
        self.Dev = TCycle(20, 30)

    async def Read(self):
        R = await self.Dev.Get()
        return R[0]


class TTherm():
    def __init__(self):
        self.DevT = TDevDT(14)
        self.Hyst = THyster()

    async def Run(self, aSleep: float = 10):
        while True:
            if (await self.DevT.Check() == True):
                State = self.Hyst.CheckP(25, self.DevT.Val)
                await Plugin.Post(self, [self.DevT.Val, State])

            await asyncio.sleep(aSleep)
