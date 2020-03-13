'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.12
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
#
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks


class TTaskDoorCheck(TTask):
    def __init__(self, aPinBtn, aPinLed, aPinSnd):
        self.PinSnd = aPinSnd
        self.PinLed = aPinLed
        self.Last = 1
        self.CntDoor = 0

        self.Obj = machine.Pin(aPinBtn, machine.Pin.IN)
        self.Beep()

    def Beep(self):
        Delay = 0.15
        UHrd.LedFlash(self.PinLed, 2, Delay)
        UHrd.LedFlash(self.PinSnd, 4, Delay)

    def tCheck(self):
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

    def DoLoop(self):
        self.tCheck()
