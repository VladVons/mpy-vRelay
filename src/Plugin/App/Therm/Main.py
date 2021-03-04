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


class TTherm():
    def __init__(self):
        self.Hyst = THyster()

        if (Conf.Alias == 'dht22-t'):
            from IncP.DevC.Dht22 import TDevDT
            self.DevT = TDevDT(14)
        else:
            from IncP.DevC.EmuCycle import TDevCycle
            self.DevT = TDevCycle(20, 30)

    async def Run(self, aSleep: float = 10):
        while True:
            if (await self.DevT.Check() == True):
                State = self.Hyst.CheckP(25, self.DevT.Val)
                await Plugin.Post(self, [self.DevT.Info(), State])

            await asyncio.sleep(aSleep)
