'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


from machine import Pin
import uasyncio as asyncio
#
from Inc.Conf import Conf


class TIdle():
    CntLoop = 0

    def tLedBeat(self):
        O = Pin(2, Pin.OUT)
        O.value(not O.value())

    async def Run(self, aSleep: float = 2):
        while True:
            print('Idle', self.CntLoop)
            self.tLedBeat()

            self.CntLoop += 1
            await asyncio.sleep(aSleep)
