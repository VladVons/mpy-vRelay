'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
import time
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


def LedFlash(aCnt: int = 4):
    O = machine.Pin(2, machine.Pin.OUT)
    for i in range(aCnt * 2):
        O.value(not O.value())
        time.sleep(0.2)
    O.value(0)


class TWDog:
    def __init__(self, aID: int, aTOut: int):
        self._TOut = aTOut
        self._Cnt  = 0
        Timer = machine.Timer(aID)
        Timer.init(period = int(1 * 1000), mode = machine.Timer.PERIODIC, callback = self._CallBack)

    def _CallBack(self, aTimer):
        self._Cnt += 1
        Log.Print(1, 'TWDog _CallBack', self._Cnt)
        if (self._Cnt >= self._TOut):
            Log.Print(2, 'TWDog timeout')
            time.sleep(1)
            #aTimer.deinit()
            #machine.reset()

    def Feed(self):
        self._Cnt = 0
