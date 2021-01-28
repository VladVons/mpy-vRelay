'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
import time
import sys
import select
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


def LedFlash(aPin: int, aCnt: int, aDelay: int):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    for i in range(aCnt):
        Obj(1)
        time.sleep(aDelay)
        Obj(0)
        time.sleep(aDelay)

async def ALedFlash(aPin: int, aCnt: int, aDelay: int):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    for i in range(aCnt):
        Obj(1)
        await asyncio.sleep(aDelay)
        Obj(0)
        await asyncio.sleep(aDelay)

def GetInputChr():
    R = ''
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        R = sys.stdin.read(1)
    return R

async def GetInputStr(aPrompt = ''):
    R = ''
    while True:
        K = GetInputChr()
        if (K):
            if (ord(K) == 10): # enter
                print()
                return R
            elif (ord(K) == 27): # esc
                return ''
            elif (ord(K) == 127): # bs
                R = R[:-1]
            else:
                R += K
        sys.stdout.write("%s%s   \r" % (aPrompt, R))
        await asyncio.sleep(0.2)


class TWDog:
    def __init__(self, aID: int, aTOut: int):
        self._TOut = aTOut
        self._Cnt  = 0
        self.Enable = True

        self.Timer = machine.Timer(aID)
        self.Start()

    def Start(self):
        self.Timer.init(period = int(1 * 1000), mode = machine.Timer.PERIODIC, callback = self._CallBack)

    def Stop(self):
        self.Timer.deinit()

    def _CallBack(self, aTimer):
        if (self.Enable):
            self._Cnt += 1
            if (self._Cnt >= self._TOut):
                self.DoTimeout(aTimer)

    def DoTimeout(self, aTimer):
        Log.Print(2, 'i', 'TWDog timeout')
        time.sleep(3)
        aTimer.deinit()
        machine.reset()

    def Feed(self):
        self._Cnt = 0
 