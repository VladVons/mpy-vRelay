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
from Inc.Util import UStr, UHrd
from Inc.NetHttp import THttpServer, THttpApi
#from Inc.DB.Dbl import TDbl 


def Reset(aSec: int = 0):
    Log.Print(1, 'Reset', aSec)
    UHrd.LedFlash()
    Tasks.Stop()
    UHrd.Reset(aSec)


class THttpApiApp(THttpApi):
    def DoUrl(self, aPath, aQuery, aData):
        print('--- aPath', aPath, 'aQuery', aQuery, 'aData', aData)
        R = 'DoUrl()'

        Name, Ext = UStr.SplitPad(2, aPath.split('/')[-1], '.')
        if (Ext == 'py'):
            try:
                Obj = __import__('Api/' + Name)
                R = Obj.Api({})
            except Exception as E: 
                print('E', E)
                R = str(E)

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
        #self.WDog = UHrd.TWDog(0, 10)
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
        #self.WDog.Feed()
        pass

    def DoLoop(self):
        Log.Print(1, 'TTaskIdle %s' % self.Cnt)

        #self.tWatchDog()
        #self.tDSleep()
        self.tMemFree()
        self.tLedBeat()
        self.tConfClear()

    def DoExit(self):
        UHrd.LedFlash()


def Main():
    Log.Print(1, 'Main', os.uname())

    DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)

    if (Conf.STA_ESSID):
        from Inc.NetWLan import Connect
        if (Connect(Conf.STA_ESSID, Conf.get('STA_Paswd', ''))):
            #import upip
            #upip.install('micropython-uasyncio')

            if (not DSleep):
                from Inc.Util.UTime import SetTime
                SetTime(Conf.get('TZone', 0))

            if (Conf.Mqtt_Host):
                from Inc.NetMqtt import TTaskMqtt
                Tasks.Add(TTaskMqtt(Conf.Mqtt_Host), 0.1, 'mqtt')
            pass
        pass
    else:
        from Inc.NetCaptive import TTaskCaptive
        Tasks.Add(TTaskCaptive(), 0.1)

    Tasks.Add(THttpServer(THttpApiApp()))
    Tasks.Add(TTaskIdle(), Conf.get('FLed', 2))
    
    #time.sleep(2)
    #Reset(1*60)

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('CTRL-C')
    finally:
        Tasks.Stop()
