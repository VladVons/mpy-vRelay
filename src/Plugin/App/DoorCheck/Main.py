'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.12
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
#
from Inc.Conf import Conf
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks


class TTaskDoorCheck(TTask):
    def __init__(self, aPinBtn: int, aPinLed: int, aPinSnd: int):
        self.PinSnd: int = aPinSnd
        self.PinLed: int = aPinLed
        self.Last:int = 1
        self.CntDoor: int = 0

        self.Obj = machine.Pin(aPinBtn, machine.Pin.IN)
        self.Beep()

    async def Beep(self):
        Delay = 0.15
        await UHrd.ALedFlash(self.PinLed, 2, Delay)
        await UHrd.ALedFlash(self.PinSnd, 4, Delay)

    async def tCheck(self):
        Value = self.Obj.value()
        if (Value != self.Last):
            self.Last = Value
            if (Value == 0):
                self.CntDoor += 1
                self.Beep()

                mqtt = Tasks.Find('mqtt')
                if (mqtt):
                    print('send mqtt DoorBtn')
                    mqtt.Publish('MyTopic1', 'CntDoor %s' % self.CntDoor)

    async def DoLoop(self):
        await self.tCheck()
