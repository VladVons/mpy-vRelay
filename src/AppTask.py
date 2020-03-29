'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import os
import gc
import sys
import machine
import time
import json
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Util import UHrd
from Inc.Task import TTask, Tasks
from Inc.Util import UStr, UHrd
from Inc.NetHttp import TTaskHttpServer, THttpApi
#from App.TaskDoorCheck import TTaskDoorCheck
#from Inc.DB.Dbl import TDbl 


__version__ = '1.01'
__author__ = 'Vladimir Vons, Oster Inc.'


def Reset(aSec: int = 0):
    Log.Print(1, 'i', 'Reset', aSec)
    UHrd.LedFlash(2, 3, 0.2)
    Tasks.Stop()
    UHrd.Reset(aSec)


def Connect():
    from Inc.NetWLan import Connect

    Net = Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
    if (not Net.isconnected()):
        Net = Connect(Conf.STA_ESSID, Conf.STA_Paswd, None)
        if (Net.isconnected()):
            Conf['STA_Net'] = Net.ifconfig()
            Conf.Save()
        else:
            Reset(0)
    print(Net.ifconfig())
    return Net.isconnected()


class THttpApiApp(THttpApi):
    DirApi = 'Inc/Api'

    def DoUrl(self, aPath: str, aQuery: dict, aData: bytearray) -> str:
        print('--- aPath', aPath, 'aQuery', aQuery, 'aData', aData)
        R = 'DoUrl()'

        Name, Ext = UStr.SplitPad(2, aPath.split('/')[-1], '.')
        if (Ext == 'py'):
            try:
                Obj = __import__(self.DirApi + '/' + Name)
                R = Obj.Api(aQuery)
                R = json.dumps(R)
            except Exception as E: 
                sys.print_exception(E)
                R = Log.Print(1, 'x', 'DoUrl()', E)

        elif (aPath == '/generate_204'):
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
        #time.sleep(0.05)
        gc.collect()
        #time.sleep(0.05)
        print('mem_free Led', gc.mem_free())
        pass

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


def Run():
    Log.Print(1, 'i', 'Main', os.uname())

    DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    print('DSleep', DSleep)

    if (Conf.STA_ESSID):
        if (Connect()):
            print()

            if (not DSleep):
                from Inc.Util.UTime import SetTime
                SetTime(Conf.get('TZone', 0))

            #if (Conf.Mqtt_Host):
            #    from Inc.NetMqtt import TTaskMqtt
            #    Tasks.Add(TTaskMqtt(Conf.Mqtt_Host), 0.1, 'mqtt')
    else:
        from Inc.NetCaptive import TTaskCaptive
        Tasks.Add(TTaskCaptive(), 0.1)

    Tasks.Add(TTaskHttpServer(THttpApiApp()), aAlias = 'http')
    Tasks.Add(TTaskIdle(), Conf.get('TIdle', 2), 'idle')
    #Tasks.Add(TTaskDoorCheck(Conf.get('PinBtn', 0), Conf.get('PinLed', 2), Conf.get('PinSnd', 13)), 0.5, 'door')

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('CTRL-C')
    finally:
        Tasks.Stop()