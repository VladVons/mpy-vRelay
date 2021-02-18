'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.18
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
#
from Inc.Mqtt import MQTTClient
from Inc.Plugin import Plugin
from Inc.ApiParse import QueryToDict, QueryUrl
from Inc.Util.UStr import SplitPad


class TMqtt():
    async def DoSubscribe(self, aTopic: str, aMsg):
        Path, Query = SplitPad(2, aMsg.decode('utf-8'), '?')
        Query = QueryToDict(Query)
        R = await QueryUrl(Path, Query)
        print('DoSubscribe', aTopic, aMsg, R)

        await Plugin.Post(self, [aTopic, aMsg])

    def Publish(self, aTopic: str, aMsg: str):
        print('Publish', aTopic, aMsg)
        self.Mqtt.publish(aTopic, aMsg)

    async def Run(self, aHost: str, aPort: int = 1883, aUser: str = None, aPassword: str = None):
        self.Mqtt = Mqtt = MQTTClient('ID-1', aHost, aPort, aUser, aPassword)
        Mqtt.set_callback(self.DoSubscribe)
        while True:
            Mqtt.connect()
            await Mqtt.subscribe('aTopic')
            try:
                while True:
                    await Mqtt.check_msg()
                    await asyncio.sleep(0.2)
            finally:
                Mqtt.disconnect()
