'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT11 temperature-humidity sensor
'''


from Inc.Dev.dht11 import DHT11
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Exec(self, aPin: int) -> dict:
        try:
            Obj = DHT11(aPin)
            R = Obj.Get()
        except Exception as E:
            R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    def Query(self, aData: dict) -> dict:
        Pin = int(aData.get('pin', '14'))
        return self.Exec(Pin)
