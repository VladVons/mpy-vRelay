import uasyncio as asyncio
from machine import WDT


async def Run():
    wdt = WDT()
    while True:
        wdt.feed()
        await asyncio.sleep(0.1)
