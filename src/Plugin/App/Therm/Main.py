'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description: 
'''


import uasyncio as asyncio
import time
#
from . import Conf
from App import ConfApp, ConfDevApp
from Inc.Plugin import Plugin
from Inc.Log  import Log

class TTherm():
    #async def _DoPost(self, aOwner, aMsg):
    #    self.Cron.Set(aMsg.get('Val'))
    #    pass

    async def _DoStop(self, aOwner, aMsg):
        print('TTherm._DoStop')

    async def Check(self):
        CD = ConfDevApp
        Temper1 = CD.Temper1
        Hyster1 = CD.Hyster1
        Cron1 = CD.Cron1
        Heat1 = CD.Heat1
        Led1 = CD.Led1

        if (await Temper1.Check() == True):
            Info = dict(Temper1.Info(), **{'Uptime': int(time.ticks_ms() / 1000)})
            await Plugin.Post(self, Info)

        #print(self.DevT.Val)
        Cron1.Init(Conf.Cron)
        CronVal = await Cron1.Get()
        if (CronVal is None):
            await Heat1.Set(0)
        else:
            On = Hyster1.CheckP(CronVal, Temper1.Val)
            await Heat1.Set(On)
            await Led1.Set(On)
            print('---Temp %s, On %s' % (Temper1.Val, On))

    async def Run(self, aSleep: float = 5):
        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
