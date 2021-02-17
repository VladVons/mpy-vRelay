import uasyncio as asyncio
from machine import WDT


class TWDog():
    async def Run(self):
        wdt = WDT()
        while True:
            wdt.feed()
            await asyncio.sleep(0.5)

    async def _DoPost(self, aOwner, aMsg):
        print('Im TWDog', aOwner, aMsg)
