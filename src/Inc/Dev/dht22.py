'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT22 temperature-humidity sensor
'''

import machine
import dht
import time


class DHT22():
    def __init__(self, aPin):
        Pin = machine.Pin(aPin)
        self.Obj = dht.DHT22(Pin)

    def Get(self):
        time.sleep_ms(100)
        self.Obj.measure()
        time.sleep_ms(250)
        return [self.Obj.temperature(), self.Obj.humidity()]
