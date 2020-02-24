'''
Author:      Vladimir Vons <VladVons@gmail.com>, Oster Inc
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
from Inc.Task import TTask
from Inc      import UStr, UHrd
from Inc.HttpServer import THttpServer, THttpApi

ELoop = asyncio.get_event_loop()


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

    def ConfClear(self):
        Btn = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        if (not Btn.value()):
            self.BtnCnt += 1
            if (self.BtnCnt > 2):
                print('Reset')

                Conf['STA_ESSID'] = ''
                Conf.Save()

                UHrd.LedFlash()
                machine.reset()
        else:
            self.BtnCnt = 0 

    def DoRun(self):
        print('Task_Led', self.Cnt)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        Obj = machine.Pin(2, machine.Pin.OUT)
        Obj.value(not Obj.value())

        if (self.Cnt % 20 == 0):
            print('DSleep')
            self.DoExit()
            UHrd.DeepSleep(Conf.DSleep)

        self.ConfClear()

    def DoExit(self):
        UHrd.LedFlash()


def InitServer():
    if (machine.reset_cause() == machine.DEEPSLEEP_RESET):
        Log.Print(1, 'From  DSleep')
    else:
        Log.Print(1, 'From reset')

        if (not Conf.STA_ESSID):
            from Inc.NetCaptive import TTaskCaptive
            Task = TTaskCaptive()
            ELoop.create_task(Task.Run())
        else:
            from Inc.NetWLan import Connect
            Connect(Conf.STA_ESSID, Conf.STA_Paswd)

    Task = THttpServer(THttpApiApp())
    ELoop.create_task(Task.Run())


def Main():
    Log.Print(1, 'Main', os.uname())

    InitServer()

    Task = TTaskIdle()
    Task.Sleep = Conf.FLed
    ELoop.create_task(Task.Run())

    ELoop.run_forever()
