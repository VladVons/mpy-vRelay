'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT11 temperature-humidity sensor
'''


from Inc.Log import Log
from Inc.Dev.dht11 import DHT11


def Api(aData: dict) -> dict:
    aPin = int(aData.get('pin', '14'))
    try:
        Obj = DHT11(aPin)
        R = Obj.Get()
    except Exception as E:
        Log.Print(1, 'x', 'dht11.Api()', E)
        R = [None, None]
    return {'temperature': R[0], 'humidity': R[1]}
