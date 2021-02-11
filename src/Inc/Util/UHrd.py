'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
import uasyncio as asyncio
#
from Inc.Log  import Log


def Reset(aSec: int):
    if (aSec > 0):
        O = machine.RTC()
        O.irq(trigger = O.ALARM0, wake = machine.DEEPSLEEP)
        O.alarm(O.ALARM0, aSec * 1000)
        machine.deepsleep()
    else:
        machine.reset()


async def LedFlash(aPin: int, aCnt: int, aDelay: int):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    for i in range(aCnt):
        Obj(1)
        await asyncio.sleep(aDelay)
        Obj(0)
        await asyncio.sleep(aDelay)
