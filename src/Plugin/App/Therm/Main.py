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
from IncP.Dev.Gpio import GpioW


class TTherm():
    def __init__(self):
        self.Hyst = THyster(2.0)
        self.Cron = TCron()

        PinOut = ConfApp.PinOut.get('heat-a')
        self.Heat = GpioW(PinOut)

        PinOut = ConfApp.PinOut.get('dht22-a')
        if (PinOut):
            from IncP.DevC.Sen_dht22 import TSen_dht22_t
            self.DevT = TSen_dht22_t(PinOut)
        else:
            PinOut = ConfApp.PinOut.get('ds18b20-a')
            if (PinOut):
                from IncP.DevC.Sen_ds18b20 import TSen_ds18b20
                self.DevT = TSen_ds18b20(PinOut)
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

            CronVal = self.Cron.GetVal()
            if (CronVal is None):
                await self.Heat.Set(0)
            else:
                On = self.Hyst.CheckP(CronVal, self.DevT.Val)
                await self.Heat.Set(On)

    async def Run(self, aSleep: float = 5):
        self.Cron.Set(ConfTherm.Cron)

        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
