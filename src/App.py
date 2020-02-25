'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import os
import gc
import machine
import time
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Task import TTask, Tasks
from Inc      import UStr, UHrd
from Inc.NetHttp import THttpServer, THttpApi


def Reset(aDSleep: bool = False):
    UHrd.LedFlash()
    Tasks.Stop()
    if (aDSleep):
        UHrd.DSleep(Conf.DSleep)
    else:
        machine.reset()


class THttpApiApp(THttpApi):
    def DoUrl(self, aPath, aQuery, aData):
        print('--- aPath', aPath, 'aQuery', aQuery, 'aData', aData)

        if (aPath == '/generate_204'):
            aPath += '.html' 

            R = super().DoUrl(aPath, aQuery, aData)
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)
        elif (aPath == '/login'):
            Query = self.ParseQuery(aData.decode('utf-8'))
            Conf['STA_ESSID'] = Query.get('STA_ESSID')
            Conf['STA_Paswd'] = Query.get('STA_Paswd')
            Conf.Save()
            Reset()
        else:
            R = super().DoUrl(aPath, aQuery, aData)
        return R


class TTaskIdle(TTask):
    BtnCnt = 0
    Sleep  = Conf.FLed

    def tLedBeat(self):
        O = machine.Pin(2, machine.Pin.OUT)
        O.value(not O.value())

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
        if (Conf.DSleep) and (self.Cnt % 20 == 0):
            Reset(True)

    def tMemFree(self):
        gc.collect()
        print('mem_free Led', gc.mem_free())

    def DoLoop(self):
        Log.Print(1, 'TTaskIdle %s' % self.Cnt)

        self.tMemFree()
        self.tLedBeat()
        self.tConfClear()
        self.tDSleep()

    def DoExit(self):
        UHrd.LedFlash()



def Main():
    Log.Print(1, 'Main', os.uname())

    DSleep = machine.reset_cause() == machine.DEEPSLEEP_RESET

    if (Conf.STA_ESSID):
        from Inc.NetWLan import Connect
        if (Connect(Conf.STA_ESSID, Conf.STA_Paswd)):
            from ntptime import settime
            settime()

            if (Conf.Mqtt_Host):
                from Inc.NetMqtt import TTaskMqtt
                Tasks.Add(TTaskMqtt(Conf.Mqtt_Host))
    else:
        from Inc.NetCaptive import TTaskCaptive
        Tasks.Add(TTaskCaptive())

    Tasks.Add(THttpServer(THttpApiApp()))
    Tasks.Add(TTaskIdle())

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('CTRL-C')
    finally:
        Tasks.Stop()
