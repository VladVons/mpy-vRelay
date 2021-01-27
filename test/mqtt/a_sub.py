#!/usr/bin/env python


import os
import signal
import asyncio
import time
from gmqtt import Client as MQTTClient

import sys
sys.path.append('../src')
from Inc.Log import Log, TEchoFile
Log.AddEcho(TEchoFile('a_sub.py.log'))
Log.Print(1, 'start', 0)


AEvent = asyncio.Event()


async def TaskPulse():
    Cnt = 0
    while True:
        Cnt += 1
        print('TaskPulse', Cnt)
        await asyncio.sleep(5)


def ask_exit(*args):
    AEvent.set()


class TMqtt():
    def on_connect(self, client, flags, rc, properties):
        client.subscribe(self.Topic, qos=1)
        print('on_connect()')

    def on_message(self, client, topic, payload, qos, properties):
        #print('on_message()', topic, payload.decode(), properties)
        Log.Print(1, topic, round(time.time() - self.Last, 1))
        self.Last = time.time()

    async def Main(self, aHost, aToken, aTopic):
        print('Main()', aHost, aToken)

        self.Topic = aTopic
        self.Last = time.time()

        client = MQTTClient('asdfghjk')
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        #client.set_auth_credentials(aToken, None)
        await client.connect(aHost, 1883, keepalive=60)
        #client.publish(TOPIC, 'Message payload', response_topic='RESPONSE/TOPIC')
        #client.publish(TOPIC, 'Message payload', response_topic=TOPIC)

        await AEvent.wait()
        await client.disconnect()



loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, ask_exit)
loop.add_signal_handler(signal.SIGTERM, ask_exit)

#loop.create_task(TaskPulse())

Mqtt = TMqtt()
token = os.environ.get('FLESPI_TOKEN')
TaskMain = Mqtt.Main('vpn2.oster.com.ua', token, 'MyTopic')

loop.run_until_complete(TaskMain)
