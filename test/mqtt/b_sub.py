#!/usr/bin/env python

import logging
import asyncio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1


Host = 'mqtt://vpn2.oster.com.ua'
Topic = 'vRelay/#'

class TServer():
    async def Run(self):
        while True:
            Client = MQTTClient('vRelay-srv')
            await Client.connect(Host)
            await Client.subscribe([(Topic, QOS_1)])

            try:
                i = 0
                while True:
                    Message = await Client.deliver_message()
                    Packet = Message.publish_packet
                    print(f"{i}:  {Packet.variable_header.topic_name} => {Packet.payload.data}")
                    i += 1
            except ClientException as E:
                await Client.unsubscribe([Topic])
                await Client.disconnect()
                logging.error("Client exception: %s" % E)


asyncio.run(TServer().Run())

