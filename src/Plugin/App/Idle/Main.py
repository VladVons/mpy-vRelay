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

#Pins = [0, 2, 4, 5, 12, 13, 14, 15]

class TIdle():
    CntLoop = 0

    #async def tPinBeat(self):
    #    PinNo = Pins[0]
    #    Pins.append(Pins.pop(0))
    #    for x in [False, True]:
    #        print('PinNo', PinNo, x)
    #        O = Pin(PinNo, Pin.OUT)
    #        O.value(x)
    #        await asyncio.sleep(2)


    def tMemInfo(self):
        gc.collect()
        print('Idle', self.CntLoop, 'MemFree', gc.mem_free())

    def tLedBeat(self):
        O = Pin(2, Pin.OUT)
        O.value(not O.value())

    async def Run(self, aSleep: float = 2):
        while True:

            self.tMemInfo()
            self.tLedBeat()
            #await self.tPinBeat()

            self.CntLoop += 1
            await asyncio.sleep(aSleep)
