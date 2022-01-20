'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.10
License:     GNU, see LICENSE for more details
'''


import uasyncio as asyncio
from machine import WDT


class TWDog():
    async def Run(self, aSleep: float = 0.5):
        wdt = WDT()
        while True:
            wdt.feed()
            await asyncio.sleep(aSleep)
