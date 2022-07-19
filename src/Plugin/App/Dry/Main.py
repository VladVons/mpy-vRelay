'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.07.19
License:     GNU, see LICENSE for more details
Description:
'''


import uasyncio as asyncio
import time
#
from Inc.Plugin import Plugin
from IncP.Log import Log


class TDry():
    async def Check(self):
        On = await self.CC.Cron1.Get()
        print('--x2', On)

    async def Run(self, aSleep: float = 1):
        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
