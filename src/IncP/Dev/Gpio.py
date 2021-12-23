'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.12.22
License:     GNU, see LICENSE for more details
Description:.
'''

from machine import Pin
import uasyncio as asyncio


Lock = asyncio.Lock()


class GpioR():
    def __init__(self, aPin: int):
        self.Obj = Pin(aPin, Pin.IN)

    async def Get(self):
        async with Lock:
            return self.Obj.value()

class GpioW():
    def __init__(self, aPin: int):
        self.Obj = Pin(aPin, Pin.OUT)

    async def Set(self, aVal: int):
        async with Lock:
            self.Obj.value(aVal)

    async def Get(self):
        async with Lock:
            return self.Obj.value()
