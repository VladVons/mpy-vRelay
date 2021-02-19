'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.18
License:     GNU, see LICENSE for more details
Description:.
'''

import json
import uasyncio as asyncio
#
from Inc.Mqtt import MQTTClient
from Inc.Plugin import Plugin
from Inc.ApiParse import QueryToDict, QueryUrl
from Inc.Util.UStr import SplitPad


class TMqtt():
    async def DoSubscribe(self, aTopic: str, aMsg):
        tId, tType, tApi = SplitPad(3, aTopic.decode('utf-8'), '/')
        if (tApi == 'Url'):
            Path, Query = SplitPad(2, aMsg.decode('utf-8'), '?')
            Query = QueryToDict(Query)
            R = await QueryUrl(Path, Query)
        else:
            R = await Plugin.Post(self, [tApi.replace('.', '/'), aMsg])

        #print('DoSubscribe', aTopic, aMsg, R)
        await self.Publish('%s/pub/%s' % (tId, tApi), json.dumps(R))

    async def Publish(self, aTopic: str, aMsg: str):
        #print('Publish', aTopic, aMsg)
        await self.Mqtt.publish(aTopic, aMsg)

    async def Run(self, aHost: str, aPort: int = 1883, aUser: str = None, aPassword: str = None):
        self.Mqtt = Mqtt = MQTTClient('ID-1', aHost, aPort, aUser, aPassword)
        Mqtt.set_callback(self.DoSubscribe)
        while True:
            Mqtt.connect()
            #await Mqtt.subscribe('Topic')
            await Mqtt.subscribe('vRelay/sub/#')
            try:
                while True:
                    await Mqtt.check_msg()
                    await asyncio.sleep(0.2)
            finally:
                Mqtt.disconnect()
