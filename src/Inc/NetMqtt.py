'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:.
'''


import uasyncio as asyncio
from umqtt.simple import MQTTClient
#
from .Log import Log
from .Task import TTask, Tasks


class TTaskMqtt(TTask):
    def __init__(self, aHost, aPort = 1883):
        self.O = MQTTClient('ClientID', aHost, aPort)
        self.O.set_callback(self.OnMessage)

    def Publish(self, aTopic: str, aMsg: str):
        try:
            self.O.publish(aTopic, aMsg)
        except: pass

    def OnMessage(self, aTopic, aMsg):
        print('OnMessage', aTopic, aMsg)
        Tasks.Post(self, {'Type': 'OnMsg', 'Param': [aTopic, aMsg]})

    def DoEnter(self):
        Log.Print(1, 'Mqtt.DoEnter')

        self.O.connect()
        Log.Print(1, 'Mqtt connect')

        aTopic = 'MyTopic'
        self.O.subscribe(aTopic)

    def DoLoop(self):
        self.O.check_msg()

    def DoExit(self):
        try:
            self.O.disconnect()
        except: pass

    def DoExcept(self, aE):
        Log.Print(1, 'Mqtt DoExcept', aE)
        return 30
