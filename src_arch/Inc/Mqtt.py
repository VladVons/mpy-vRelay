'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:.
'''


import uasyncio as asyncio
from umqtt.simple import MQTTClient
import time
import sys
#
from .Log import Log
from .Task import TTask, Tasks


def SendTo(aHost: str, aTopic: str, aMsg):
    Obj = MQTTClient('ClientID', aHost, 1883)
    try:
        Obj.connect()
        Obj.publish(aTopic, aMsg)
        Obj.disconnect()
        Log.Print(1, 'i', 'Mqtt OK')
    except Exception as E:
        Log.Print(1, 'x', 'Mqtt Err', E)


class TTaskMqtt(TTask):
    def __init__(self, aHost: str, aPort: int = 1883, aUser: str = None, aPassword: str = None):
        self.O = MQTTClient('ClientID', aHost, aPort, aUser, aPassword)
        self.O.set_callback(self.OnMessage)

    def Publish(self, aTopic: str, aMsg: str):
        try:
            self.O.publish(aTopic, aMsg)
        except: pass

    def OnMessage(self, aTopic: str, aMsg):
        print('OnMessage', aTopic, aMsg)
        Tasks.Post(self, {'Type': 'OnMsg', 'Param': [aTopic, aMsg]})

    async def DoEnter(self):
        Log.Print(1, 'i', 'Mqtt.DoEnter')

        self.O.connect()
        Log.Print(1, 'i', 'Mqtt connect')

        aTopic = 'MyTopic'
        self.O.subscribe(aTopic)

    async def DoLoop(self):
        self.O.check_msg()

    async def DoExit(self):
        try:
            self.O.disconnect()
        except: pass
