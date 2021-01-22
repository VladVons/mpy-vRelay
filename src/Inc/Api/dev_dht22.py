'''
Author:      Vladimir Vons, Oster Inc
Created:     2018.02.11
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT22 temperature-humidity sensor

https://forum.micropython.org/viewtopic.php?f=14&t=4876&p=28035#p28035
https://forum.micropython.org/viewtopic.php?f=15&t=4877&p=28043#p28043
'''

from Inc.Dev.dht22 import DHT22
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    def Exec(self, aPin: int) -> dict:
        try:
            Obj = DHT22(aPin)
            R = Obj.Get()
        except Exception as E:
            Log.Print(1, 'Err: dev_dht22', 'Api()', E)
            R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    def Query(self, aData: dict) -> dict:
        Pin = int(aData.get('pin', '14'))
        return self.Exec(Pin)
