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
from Inc.Log  import Log
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.Sender import TSender
from Inc.ApiParse import QueryToDict, QueryUrl
from Inc.Util.UStr import SplitPad
from IncP.Marker import Marker


cName = 'vRelay'


class TMqtt():
    async def _DoPost(self, aOwner, aMsg):
        Data = Marker(self, aOwner, aMsg)
        await self.Sender.Send(('%s/pub/%s' % (cName, 'post'), Data))

    async def Send(self, aData):
        if (self.Mqtt.is_connected()):
            print('Send', aData)

            Topic, Data = aData
            try:
                await self.Mqtt.publish(Topic, json.dumps(Data))
                return True
            except Exception as E:
                Log.Print(1, 'x', 'Send()', E)

    async def DoSubscribe(self, aTopic: str, aMsg):
        aMsg = aMsg.decode('utf-8')
        tId, tType, tApi = SplitPad(3, aTopic.decode('utf-8'), '/')
        if (tApi == 'Url'):
            Path, Query = SplitPad(2, aMsg, '?')
            Query = QueryToDict(Query)
            R = await QueryUrl(Path, Query)
        else:
            R = await Plugin.Post(self, (tApi.replace('.', '/'), aMsg))

        #Log.Print(1, 'i', 'DoSubscribe()', 'topic: %s, msg: %s, res: %s' % (aTopic, aMsg, R))
        await self.Sender.Send(('%s/pub/%s' % (tId, tApi), R))

    async def Run(self, aSleep: float = 1.0):
        ConnMod = 'App.ConnSTA'
        ConnSTA = Plugin.Get(ConnMod)[0]

        self.Mqtt = Mqtt = MQTTClient('%s-%s' % (cName, ConnSTA.Mac()) , Conf.Mqtt_Host, Conf.get('Mqtt_Port', 1883), Conf.Mqtt_User, Conf.Mqtt_Passw)
        Mqtt.set_callback(self.DoSubscribe)

        self.Sender = TSender(self.Send)
        await self._DoPost(self, 'start')

        while True:
            try:
                await ConnSTA.Event.wait()

                Mqtt.disconnect()
                Mqtt.connect()
                await Mqtt.subscribe('%s/sub/#' % (cName))
                while True:
                    # simlify nesting. too many recursion
                    #await Mqtt.check_msg()
                    Mqtt.sock.setblocking(False)
                    await Mqtt.wait_msg()

                    await asyncio.sleep(aSleep)
            except Exception as E:
                Log.Print(1, 'x', 'TMqtt.Run()', E)

            await asyncio.sleep(aSleep)
