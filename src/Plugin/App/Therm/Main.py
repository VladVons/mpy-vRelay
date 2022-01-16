'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description: 
'''


import uasyncio as asyncio
import time
#
from Inc.Plugin import Plugin
from Inc.Log  import Log

class TTherm():
    async def _DoPost(self, aOwner, aMsg):
        #print('TTherm._DoPost', aOwner, aMsg)
        #self.Cron.Set(aMsg.get('Val'))
        pass

    async def _DoStop(self, aOwner, aMsg):
        print('TTherm._DoStop', aOwner, aMsg)

    async def Check(self):
        CC = self.CC
        Temper1 = CC.Temper1
        Hyster1 = CC.Hyster1
        Cron1 = CC.Cron1
        Heat1 = CC.Heat1
        Led1 = CC.Led1

        if (await Temper1.Check() == True):
            Info = dict(Temper1.Info(), **{'Uptime': int(time.ticks_ms() / 1000)})
            await Plugin.Post(self, Info)

        #print(self.DevT.Val)
        Cron1.Init(CC.Conf.Cron)
        CronVal = await Cron1.Get()
        if (CronVal is None):
            await Heat1.Set(0)
        else:
            On = Hyster1.CheckP(CronVal, Temper1.Val)
            await Heat1.Set(On)
            await Led1.Set(On)
            print('---Temp %s, On %s' % (Temper1.Val, On))

    async def Run(self, aSleep: float = 15):
        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
