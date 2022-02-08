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
        Alias = 'Button1'
        Data = aMsg.get('Data', {})
        if (Data.get('Alias') == Alias):
            Val = Data.get('Val')
            if (Val == -1):
                if (Alias in self.CC.Heat1.Allow):
                    self.CC.Heat1.Allow.remove(Alias)
            else:
                if (not Alias in self.CC.Heat1.Allow):
                    self.CC.Heat1.Allow.append(Alias)

                await self.CC.Heat1.Set(Val, Alias)
                await self.CC.Led1.Set(Val)


    #async def _DoStop(self, aOwner, aMsg):
    #    print('TTherm._DoStop', aOwner, aMsg)

    async def Check(self):
        CC = self.CC
        Temp1 = CC.Temp1
        Hyster1 = CC.Hyster1
        Cron1 = CC.Cron1
        Heat1 = CC.Heat1
        Led1 = CC.Led1

        if (await Temp1.Check() == True):
            Info = dict(Temp1.Info(), **{'Uptime': int(time.ticks_ms() / 1000)})
            await Plugin.Post(self, Info)

        #print(self.DevT.Val)
        Cron1.Init(CC.Conf.Cron)
        CronVal = await Cron1.Get()
        if (CronVal is None):
            await Heat1.Set(0)
        else:
            On = Hyster1.CheckP(CronVal, Temp1.Val)
            await Heat1.Set(On, 'Hyster1')
            await Led1.Set(On)
            print('---Temp %s, On %s' % (Temp1.Val, On))

    async def Run(self, aSleep: float = 15):
        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
