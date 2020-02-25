'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:.
'''


import uasyncio as asyncio
from umqtt.simple import MQTTClient
#
from Inc.Log import Log
from Inc.Task import TTask


class TTaskMqtt(TTask):
    def __init__(self, aHost, aPort = 1883):
        self.Sleep = 0.1

        aTopic = 'MyTopic'
        O = MQTTClient('ClientID', aHost, aPort)
        O.set_callback(self.on_message)
        O.connect()
        O.publish(aTopic, "ESP8266 is Connected")
        O.subscribe(aTopic)
        self.O = O

    def on_message(self, aClient, aMessage):
        print ('on_message')
        #print ('on_message', aMessage.topic, aMessage.payload)

    def DoLoop(self):
        self.O.check_msg()

    def DoExit(self):
        self.O.disconnect()
