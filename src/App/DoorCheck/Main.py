'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.12
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
import uasyncio as asyncio
#
from Inc.Plugin import Plugin
from Inc.Util import UHrd


class TDoorCheck():
    def __init__(self, aPinBtn: int, aPinLed: int, aPinSnd: int):
        self.PinSnd: int = aPinSnd
        self.PinLed: int = aPinLed
        self.Last:int = 1
        self.CntDoor: int = 0

        self.Obj = machine.Pin(aPinBtn, machine.Pin.IN)
        self.Beep()

    async def Beep(self):
        Delay = 0.15
        await UHrd.LedFlash(self.PinLed, 2, Delay)
        await UHrd.LedFlash(self.PinSnd, 4, Delay)

    async def tCheck(self):
        Value = self.Obj.value()
        if (Value != self.Last):
            self.Last = Value
            if (Value == 0):
                self.CntDoor += 1
                self.Beep()

                Mqtt = Plugin.Get('App/Mqtt')
                if (Mqtt):
                    Mqtt.Publish('MyTopic1', 'CntDoor %s' % self.CntDoor)

    async def Run(self, aSleep: int = 1):
        while True:
            await self.tCheck()
            await asyncio.sleep(aSleep)
