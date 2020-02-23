'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.02.11
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT22 temperature-humidity sensor

https://forum.micropython.org/viewtopic.php?f=14&t=4876&p=28035#p28035
https://forum.micropython.org/viewtopic.php?f=15&t=4877&p=28043#p28043
'''

import machine
import time
import dht
#
from Log import Log


def Get(aPin):
    #Pin = machine.Pin(aPin, machine.Pin.IN, machine.Pin.PULL_UP)
    Pin = machine.Pin(aPin)
    Obj = dht.DHT22(Pin)

    try:
        time.sleep_ms(250)
        Obj.measure()
        time.sleep_ms(250)
        T = Obj.temperature()
        H = Obj.humidity()
        R = [T, H]
    except Exception as e:
        Log.Print(1, 'Err: DevDHT22', 'Get()', e)
        R = [None, None]
    return R


def Api(aData):
    aPin = aData.get('pin', 0)
    R = Get(aPin)
    return {'temperature': R[0], 'humidity': R[1]}
