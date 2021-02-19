'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import gc
from network import WLAN, STA_IF
from machine import Pin
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.Log  import Log
from App.Utils import TWLanApp


class TIdle():
    CntLoop = 0
    CntBtn = 0

    def tLedBeat(self):
        O = Pin(2, Pin.OUT)
        O.value(not O.value())

        #if (self.CntLoop % 5 == 0):
        #    mqtt = Tasks.Find('mqtt')
        #    if (mqtt):
        #        print('mqtt public')
        #        mqtt.Publish('MyTopic1', 'tLedBeat %s' % self.CntLoop)

    def tConfClear(self):
        O = Pin(0, Pin.IN, Pin.PULL_UP)
        if (not O.value()):
            self.CntBtn += 1
            if (self.CntBtn > 2):
                Conf['STA_ESSID'] = ''
                Conf.Save()

                from App.Utils import Reset
                Reset()
        else:
            self.CntBtn = 0 

    def tDSleep(self):
        if (Conf.DSleep) and (self.CntLoop % 60 == 0):
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
        if (Cnt > 0) and (self.CntLoop % Cnt == 0):
            WLan = TWLanApp()
            await WLan.CheckConnect()

    #async def DoExit(self):
        #WDog.Stop()
        #from Inc.Util import UHrd
        #await UHrd.LedFlash(2, 3, 0.2)

    #async def DoPost(self, aOwner: TTask, aMsg):
    #    print('InIdle', aOwner.Alias, aMsg)

    async def _DoPost(self, aOwner, aMsg):
        print('Im Idle', aOwner, aMsg)
        return 'from Idle'

    async def Run(self, aSleep: float = 2):
        while True:
            await self.tWatchHost()
            await self.tWatchConnect()
            #self.tDSleep()
            #self.tMemFree()
            self.tLedBeat()
            self.tConfClear()

            self.CntLoop += 1
            await asyncio.sleep(aSleep)

            #if (self.CntLoop % 3 == 0):
                #await Plugin.Post(self, 'from Idle')
                #Obj = Plugin.Get('App/Mqtt')
                #if (Obj):
                #    Obj.Publish('aTopic1', self.CntLoop)
