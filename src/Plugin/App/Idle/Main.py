'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import gc
from network import WLAN, STA_IF
from machine import Pin
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks
from App.Utils import Reset
from App.Utils import TWLanApp


class TTaskIdle(TTask):
    BtnCnt = 0

    def tLedBeat(self):
        O = Pin(2, Pin.OUT)
        O.value(not O.value())

        if (self.Cnt % 5 == 0):
            mqtt = Tasks.Find('mqtt')
            if (mqtt):
                print('mqtt public')
                mqtt.Publish('MyTopic1', 'tLedBeat %s' % self.Cnt)

    def tConfClear(self):
        O = Pin(0, Pin.IN, Pin.PULL_UP)
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
        print('mem_free', gc.mem_free())

        Net = WLAN(STA_IF)
        print('ifconfig', Net.ifconfig()[0])

    async def tWatchConnect(self):
        Net = WLAN(STA_IF)
        if (not Net.isconnected):
            WLan = TWLanApp()
            await WLan.TryConnect()

    async def tWatchHost(self):
        Cnt = Conf.get('WatchHost_Cnt', 0)
        if (Cnt > 0) and (self.Cnt % Cnt == 0):
            WLan = TWLanApp()
            await WLan.CheckConnect()

    async def DoLoop(self):
        #Log.Print(1, 'i', 'TTaskIdle %s' % self.Cnt)

        await self.tWatchHost()
        await self.tWatchConnect()
        #self.tDSleep()
        #self.tMemFree()
        self.tLedBeat()
        self.tConfClear()

    async def DoExit(self):
        #WDog.Stop()
        await UHrd.LedFlash(2, 3, 0.2)

    async def DoPost(self, aOwner: TTask, aMsg):
        print('InIdle', aOwner.Alias, aMsg)
