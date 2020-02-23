import os
import gc
import machine
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Task import TTask
from Inc      import UStr
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
        self.Cnt += 1
        print('Task_Led', self.Cnt)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        Obj = machine.Pin(2, machine.Pin.OUT)
        Obj.value(not Obj.value())


def InitConnect():
    from Inc.NetWLan import Connect
    HttpServer = THttpServer(THttpApiApp())

    if (not Conf.STA_ESSID):
        from Inc.NetCaptive import TTaskCaptive
        TaskCaptive = TTaskCaptive()
        ELoop.create_task(TaskCaptive.Run())
    else:
        Connect(Conf.STA_ESSID, Conf.STA_Paswd)
    ELoop.create_task(HttpServer.Run())


def Main():
    Log.Print(1, 'Main', os.uname())
    InitConnect()

    TaskLed = TTaskLed()
    TaskLed.Sleep = 3
    ELoop.create_task(TaskLed.Run())

    gc.collect()
    print('mem_free', gc.mem_free())

    ELoop.run_forever()
