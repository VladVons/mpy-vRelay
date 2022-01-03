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
from Inc.ConfDev import TConfDev
from Inc.Plugin import Plugin
from Inc.Log  import Log
from Inc.Hyster import THyster
from IncP.DevC.Sen_cron import TSen_cron
from IncP.Dev.Gpio import GpioW


class TTherm():
    def __init__(self):
        self.Hyst = THyster(2.0)
        self.Cron = TSen_cron()

        PinOut = ConfApp.PinOut.get('heat-a')
        self.Heat = GpioW(PinOut)

        PinOut = ConfApp.PinOut.get('led-a')
        self.Led = GpioW(PinOut)

        ConfDev = TConfDev()
        ConfDev.Load('Conf/Dev', ConfApp)
        self.DevT = ConfDev['SenTemp']

    #async def _DoPost(self, aOwner, aMsg):
    #    self.Cron.Set(aMsg.get('Val'))
    #    pass

    async def _DoStop(self, aOwner, aMsg):
        print('TTherm._DoStop')

    async def Check(self):
        if (await self.DevT.Check() == True):
            Info = dict(self.DevT.Info(), **{'Uptime': int(time.ticks_ms() / 1000)})
            await Plugin.Post(self, Info)

        #print(self.DevT.Val)
        CronVal = await self.Cron.Get()
        if (CronVal is None):
            await self.Heat.Set(0)
        else:
            On = self.Hyst.CheckP(CronVal, self.DevT.Val)
            await self.Heat.Set(On)
            await self.Led.Set(On)
            print('---Temp %s, On %s' % (self.DevT.Val, On))

    async def Run(self, aSleep: float = 5):
        self.Cron.Init(ConfTherm.Cron)

        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
