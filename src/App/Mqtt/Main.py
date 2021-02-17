import uasyncio as asyncio
#
from Inc.Mqtt import MQTTClient
from Inc.Plugin import Plugin


class TMqtt():
    async def DoSubscribe(self, aTopic: str, aMsg):
        #print('DoSubscribe', aTopic, aMsg)
        await Plugin.Post(self, [aTopic, aMsg])

    def Publish(self, aTopic: str, aMsg: str):
        self.Mqtt.publish(aTopic, aMsg)

    async def Run(self, aHost: str, aPort: int = 1883, aUser: str = None, aPassword: str = None):
        self.Mqtt = Mqtt = MQTTClient('ID-1', aHost, aPort, aUser, aPassword)
        Mqtt.set_callback(self.DoSubscribe)
        Mqtt.connect()
        await Mqtt.subscribe('aTopic')

        while True:
            await Mqtt.check_msg()
            await asyncio.sleep(0.2)

        Mqtt.disconnect()
