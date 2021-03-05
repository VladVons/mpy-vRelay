'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.18
License:     GNU, see LICENSE for more details
Description:.
'''

import json, machine
from ubinascii import hexlify
import uasyncio as asyncio
#
from Inc.Mqtt import MQTTClient
from Inc.Log  import Log
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.ApiParse import QueryToDict, QueryUrl
from Inc.Util.UStr import SplitPad

Name = 'vRelay'


class TMqtt():
    async def _DoPost(self, aOwner, aMsg):
        Data = {
            'TMqtt': aMsg,
            'Id': hexlify(machine.unique_id()).decode('utf-8'),
            'Alias': Conf.Alias
        }
        await self.Publish('%s/pub/%s' % (Name, 'test'), json.dumps(Data))

    async def Publish(self, aTopic: str, aMsg: str):
        if (self.Mqtt.is_connected()):
            Log.Print(1, 'i', 'Publish()', 'Topic %s, Msg %s'  % (aTopic, aMsg))
            await self.Mqtt.publish(aTopic, aMsg)
            return True

    async def DoSubscribe(self, aTopic: str, aMsg):
        aMsg = aMsg.decode('utf-8')
        tId, tType, tApi = SplitPad(3, aTopic.decode('utf-8'), '/')
        if (tApi == 'Url'):
            Path, Query = SplitPad(2, aMsg, '?')
            Query = QueryToDict(Query)
            R = await QueryUrl(Path, Query)
        else:
            R = await Plugin.Post(self, [tApi.replace('.', '/'), aMsg])

        Log.Print(2, 'i', 'DoSubscribe()', 'topic: %s, msg: %s, res: %s' % (aTopic, aMsg, R))
        await self.Mqtt.publish('%s/pub/%s' % (tId, tApi), json.dumps(R))

    async def Run(self, aSleep: float = 1.0):
        ConnMod = 'App.ConnSTA'
        ConnSTA = Plugin.Get(ConnMod)[0]

        self.Mqtt = Mqtt = MQTTClient('%s-%s' % (Name, ConnSTA.Mac()) , Conf.Mqtt_Host, Conf.get('Mqtt_Port', 1883), Conf.Mqtt_User, Conf.Mqtt_Passw)
        Mqtt.set_callback(self.DoSubscribe)

        Once = True
        while True:
            try:
                await ConnSTA.Event.wait()

                Mqtt.disconnect()
                Mqtt.connect()
                await Mqtt.subscribe('%s/sub/#' % (Name))

                if (Once):
                    Once = False
                    await self._DoPost(self, 'start'):

                while True:
                    # simlify nesting. too many recursion
                    #await Mqtt.check_msg()
                    Mqtt.sock.setblocking(False)
                    await Mqtt.wait_msg()

                    await asyncio.sleep(aSleep)
            except Exception as E:
                Log.Print(1, 'x', 'TMqtt.Run()', E)

            await asyncio.sleep(aSleep)
