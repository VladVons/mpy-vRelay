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

            Log.Print(1, 'Reboot')
            UHrd.LedFlash()
            machine.reset()
        else:
            R = super().DoUrl(aPath, aQuery, aData)
        return R


class TTaskIdle(TTask):
    BtnCnt = 0
    Sleep  = Conf.FLed

    def tConfClear(self):
        O = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        if (not O.value()):
            self.BtnCnt += 1
            if (self.BtnCnt > 2):
                print('Reset')

                Conf['STA_ESSID'] = ''
                Conf.Save()

                UHrd.LedFlash()
                machine.reset()
        else:
            self.BtnCnt = 0 

    def tDSleep(self):
        if (self.Cnt % 20 == 0):
            print('DSleep')
            self.DoExit()
            UHrd.DSleep(Conf.DSleep)

    def tLedBeat(self):
        O = machine.Pin(2, machine.Pin.OUT)
        O.value(not O.value())

    def tMemFree(self):
        gc.collect()
        print('mem_free Led', gc.mem_free())

    def DoLoop(self):
        Log.Print(1, 'TTaskIdle %s' % self.Cnt)

        self.tMemFree()
        self.tLedBeat()
        self.tConfClear()
        #self.tDSleep()

    def DoExit(self):
        UHrd.LedFlash()


def InitServer():
    if (machine.reset_cause() == machine.DEEPSLEEP_RESET):
        Log.Print(1, 'Boot as DSleep')
    else:
        Log.Print(1, 'Boot as Reset')

        if (not Conf.STA_ESSID):
            from Inc.NetCaptive import TTaskCaptive
            Tasks.Add(TTaskCaptive())
        else:
            from Inc.NetWLan import Connect
            Connect(Conf.STA_ESSID, Conf.STA_Paswd)

            if (Conf.Mqtt_Host):
                from Inc.NetMqtt import TTaskMqtt
                Tasks.Add(TTaskMqtt(Conf.Mqtt_Host))

    Tasks.Add(THttpServer(THttpApiApp()))


def Main():
    Log.Print(1, 'Main', os.uname())

    InitServer()
    Tasks.Add(TTaskIdle())
    Tasks.Run()
