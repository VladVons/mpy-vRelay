'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
import time


def DSleep(aSec: int):
    O = machine.RTC()
    O.irq(trigger = O.ALARM0, wake = machine.DEEPSLEEP)
    O.alarm(O.ALARM0, aSec * 1000)
    machine.deepsleep()


def LedFlash(aCnt: int = 4):
    O = machine.Pin(2, machine.Pin.OUT)
    for i in range(aCnt * 2):
        O.value(not O.value())
        time.sleep(0.2)
    O.value(0)
