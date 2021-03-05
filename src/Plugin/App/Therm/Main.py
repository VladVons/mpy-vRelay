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
from Inc.Cron  import TCron


class TTherm():
    def __init__(self):
        self.Hyst = THyster()
        self.Cron = TCron()

        if (Conf.Alias == 'Sen_dht22'):
            from IncP.DevC.Sen_dht22 import TSen_dht22_t
            self.DevT = TSen_dht22_t(14)
        elif (Conf.Alias == 'Sen_ds18b20'):
            from IncP.DevC.Sen_ds18b20 import TSen_ds18b20
            self.DevT = TSen_ds18b20(14)
        else:
            from IncP.DevC.Emu_cycle import TEmu_cycle
            self.DevT = TEmu_cycle(20, 30)
            self.DevT.SecD = 5

    async def _DoPost(self, aOwner, aMsg):
        self.Cron.Set([])

    async def Check(self):
        if (await self.DevT.Check() == True):
            CronOk = self.Cron.IsNow()
            HystOk = self.Hyst.CheckP(25, self.DevT.Val)
            await Plugin.Post(self, self.DevT.Info())

    async def Run(self, aSleep: float = 10):
        while True:
            await self.Check()

            await asyncio.sleep(aSleep)
