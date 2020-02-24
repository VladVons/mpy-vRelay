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
            R = 'Saved\nReboot to connect'
        else:
            R = super().DoUrl(aPath, aQuery, aData)
        return R


class TTaskLed(TTask):
    Cnt = 0

    def DoRun(self):
        print('Task_Led', self.Cnt)

        self.Cnt += 1
        if (self.Cnt % 10 == 0):
            print('DSleep...')
            self.DoExit()
            UHrd.DeepSleep(Conf.DSleep)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        Obj = machine.Pin(2, machine.Pin.OUT)
        Obj.value(not Obj.value())

    def DoExit(self):
        Obj = machine.Pin(2, machine.Pin.OUT)
        for i in range(8):
            Obj.value(not Obj.value())
            time.sleep(0.2)
        Obj.value(0)


def InitConnect():
    HttpServer = THttpServer(THttpApiApp())

    if (not Conf.STA_ESSID):
        from Inc.NetCaptive import TTaskCaptive

        TaskCaptive = TTaskCaptive()
        ELoop.create_task(TaskCaptive.Run())

    if (machine.reset_cause() == machine.DEEPSLEEP_RESET):
        Log.Print(1, 'From  DSleep')
    else:
        from Inc.NetWLan import Connect

        Log.Print(1, 'From reset')
        Connect(Conf.STA_ESSID, Conf.STA_Paswd)
    ELoop.create_task(HttpServer.Run())


def Main():
    Log.Print(1, 'Main', os.uname())

    InitConnect()

    TaskLed = TTaskLed()
    TaskLed.Sleep = Conf.FLed
    ELoop.create_task(TaskLed.Run())

    gc.collect()
    print('mem_free', gc.mem_free())

    ELoop.run_forever()
