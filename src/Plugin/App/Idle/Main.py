'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import gc
import sys
import machine
import network
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks
from App.Utils import Reset


WDog = UHrd.TWDog(0, Conf.get('WatchDog', 30))

class TTaskIdle(TTask):
    BtnCnt = 0

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
        print('mem_free', gc.mem_free())

        Net = network.WLAN(network.STA_IF)
        print('ifconfig', Net.ifconfig()[0])

    def tWatchDog(self):
        WDog.Feed()

    async def tWatchHost(self):
        Cnt = Conf.get('WatchHost_Cnt', 0)
        if (Cnt > 0) and (self.Cnt % Cnt == 0):
            Net = network.WLAN(network.STA_IF)
            Host = Conf.get('WatchHost', Net.ifconfig()[2]) # or gateway

            from Inc.Util.UHttp import CheckHost
            if (not await CheckHost(Host, 80, 3)):
                from App.Utils import TWLanApp
                WLan = TWLanApp()
                for Try in range(3):
                    if (await WLan.TryConnect()):
                        return
                    await asyncio.sleep(60)

                Log.Print(1, 'i', 'WatchHost %s reset %s' % (Host, Cnt))
                await asyncio.sleep(3)
                await Reset()

    async def DoLoop(self):
        #Log.Print(1, 'i', 'TTaskIdle %s' % self.Cnt)

        self.tWatchDog()
        await self.tWatchHost()
        #self.tDSleep()
        #self.tMemFree()
        self.tLedBeat()
        self.tConfClear()

    def DoExit(self):
        WDog.Stop()
        UHrd.LedFlash(2, 3, 0.2)

    def DoPost(self, aOwner: TTask, aMsg):
        print('InIdle', aOwner.Alias, aMsg)
