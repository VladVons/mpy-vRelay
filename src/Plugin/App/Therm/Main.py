'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description:
'''


import uasyncio as asyncio
import time
#
from . import ConfTherm
from App import ConfApp
from Inc.Plugin import Plugin
from Inc.Log  import Log
from Inc.Hyster import THyster
from Inc.Cron  import TCron


class TTherm():
    def __init__(self):
        self.Hyst = THyster(2.0)
        self.Cron = TCron()

        if (ConfApp.Alias == 'Sen_dht22'):
            from IncP.DevC.Sen_dht22 import TSen_dht22_t
            self.DevT = TSen_dht22_t(14)
        elif (ConfApp.Alias == 'Sen_ds18b20'):
            from IncP.DevC.Sen_ds18b20 import TSen_ds18b20
            self.DevT = TSen_ds18b20(14)
        else:
            from IncP.DevC.Emu_cycle import TEmu_cycle
            self.DevT = TEmu_cycle(20, 30)
            self.DevT.SecD = 5

    async def _DoPost(self, aOwner, aMsg):
        #self.Cron.Set(aMsg.get('Val'))
        pass

    async def _DoStop(self, aOwner, aMsg):
        print('TTherm._DoStop')

    async def Check(self):
        if (await self.DevT.Check() == True):
            Info = dict(self.DevT.Info(), **{'Uptime': int(time.ticks_ms() / 1000)})
            await Plugin.Post(self, Info)

            Val = self.Cron.GetVal()
            if (Val is not None):
                HystOk = self.Hyst.CheckP(Val, self.DevT.Val)
                print('---ToDo. 11', Val, HystOk)
                await Plugin.Post(self, self.DevT.Info())

    async def Run(self, aSleep: float = 5):
        self.Cron.Set(ConfTherm.Cron)

        while True:
            await self.Check()

            await asyncio.sleep(aSleep)
