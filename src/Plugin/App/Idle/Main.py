'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:
'''

import gc
from machine import Pin
import uasyncio as asyncio
#
from App import ConfApp


class TIdle():
    CntLoop = 0

    def tLedBeat(self):
        O = Pin(2, Pin.OUT)
        O.value(not O.value())

    async def Run(self, aSleep: float = 2):
        while True:
            gc.collect()
            print('Idle', self.CntLoop, 'MemFree', gc.mem_free())
            self.tLedBeat()

            self.CntLoop += 1
            await asyncio.sleep(aSleep)
