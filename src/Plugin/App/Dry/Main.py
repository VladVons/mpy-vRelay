'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.07.19
License:     GNU, see LICENSE for more details
Description:
'''


import uasyncio as asyncio


class TDry():
    async def Check(self):
        On = await self.CC.Cron1.Get()
        await self.CC.Heat1.Set(On, 'Cron1')
        print('-x1', On)

    async def Run(self, aSleep: float = 1):
        for x in [True, False]:
            await self.CC.Heat1.Set(x)
            await asyncio.sleep(3)

        while True:
            await self.Check()
            await asyncio.sleep(aSleep)
