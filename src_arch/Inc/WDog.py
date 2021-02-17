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
 