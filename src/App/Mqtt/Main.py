'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.18
License:     GNU, see LICENSE for more details
Description:
'''


import json
import uasyncio as asyncio
#
from App import ConfApp
from Inc.Mqtt import MQTTClient
from Inc.Log  import Log
from Inc.Plugin import Plugin
from Inc.Sender import TSender
from Inc.ApiParse import QueryToDict, QueryUrl
from Inc.Util.UStr import SplitPad
from IncP.Marker import Marker


cName = 'vRelay'


class TMqtt():
    def __init__(self):
        self.Mqtt = None
        self.Sender = TSender(self.Send)

    async def _DoPost(self, aOwner, aMsg):
        Data = Marker(self, aOwner, aMsg)

        # call self,Send() via safe buffered sender
        await self.Sender.Send(('%s/pub/%s' % (cName, 'post'), Data))

    async def Send(self, aData) -> bool:
        if (self.Mqtt) and (self.Mqtt.is_connected()):
            Topic, Data = aData
            try:
                await self.Mqtt.publish(Topic, json.dumps(Data))
                print('TMqtt.Send', aData)
                return True
            except Exception as E:
                Log.Print(1, 'x', 'Send()', E)

    async def DoSubscribe(self, aTopic: str, aMsg):
        aMsg = aMsg.decode('utf-8')
        tId, tType, tApi = SplitPad(3, aTopic.decode('utf-8'), '/')
        if (tApi == 'Url'): # topic: vRelay/sub/Url
            Path, Query = SplitPad(2, aMsg, '?')
            Query = QueryToDict(Query)
            R = await QueryUrl(Path, Query)
        elif (tApi == 'Conf'): # topic: vRelay/sub/Conf
            Path, Query = SplitPad(2, aMsg, '?')
        else:
            print('---20', tApi, aMsg)
            R = await Plugin.Post(self, (tApi.replace('.', '/'), aMsg))

        #Log.Print(1, 'i', 'DoSubscribe()', 'topic: %s, msg: %s, res: %s' % (aTopic, aMsg, R))
        await self.Sender.Send(('%s/pub/%s' % (tId, tApi), R))

    async def Run(self, aSleep: float = 1.0):
        ConnSTA = Plugin.get('App.ConnSTA')[0]

        self.Mqtt = Mqtt = MQTTClient('%s-%s' % (cName, ConnSTA.Mac()) , ConfApp.Mqtt_Host, ConfApp.get('Mqtt_Port', 1883), ConfApp.Mqtt_User, ConfApp.Mqtt_Passw)
        Mqtt.set_callback(self.DoSubscribe)

        while True:
            try:
                await ConnSTA.Event.wait()

                Mqtt.disconnect()
                await asyncio.sleep(1)
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
