'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT11 temperature-humidity sensor
'''


from Inc.Dev.dht11 import DHT11
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    async def Exec(self, aPin: int) -> dict:
        try:
            Obj = DHT11(aPin)
            R = await Obj.Get()
        except Exception as E:
            Log.Print(1, 'Err: dev_dht11', 'Api()', E)
            R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    async def Query(self, aData: dict) -> dict:
        Pin = int(aData.get('pin', '14'))
        return await self.Exec(Pin)
