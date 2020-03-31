'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import gc
import machine
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks
from .Utils   import Reset


class TTaskIdle(TTask):
    BtnCnt = 0
 
    def __init__(self):
        self.WDog = UHrd.TWDog(0, 10)
        pass

    def tLedBeat(self):
        O = machine.Pin(2, machine.Pin.OUT)
        O.value(not O.value())

        if (self.Cnt % 5 == 0):
            mqtt = Tasks.Find('mqtt')
            if (mqtt):
                print('mqtt public')
                mqtt.Publish('MyTopic1', 'tLedBeat %s' % self.Cnt)

    def tConfClear(self):
        O = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        if (not O.value()):
            self.BtnCnt += 1
            if (self.BtnCnt > 2):
                Conf['STA_ESSID'] = ''
                Conf.Save()
                Reset()
        else:
            self.BtnCnt = 0 

    def tDSleep(self):
        if (Conf.DSleep) and (self.Cnt % 60 == 0):
            Reset(Conf.get('DSleep', 1*60))

    def tMemFree(self):
        gc.collect()
        print('mem_free Led', gc.mem_free())

    def tWatchDog(self):
        self.WDog.Feed()
        pass

    async def DoLoop(self):
        Log.Print(1, 'i', 'TTaskIdle %s' % self.Cnt)

        self.tWatchDog()
        #self.tDSleep()
        self.tMemFree()
        self.tLedBeat()
        self.tConfClear()

    def DoExit(self):
        self.WDog.Stop()
        UHrd.LedFlash(2, 3, 0.2)

    async def DoPost(self, aOwner: TTask, aMsg):
        print('InIdle', aOwner.Alias, aMsg)
