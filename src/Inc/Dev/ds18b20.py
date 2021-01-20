'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.18
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DS18X20 temperature sensor
'''
import time
import machine
import onewire
#
from   ds18x20 import DS18X20

class DS1820():
    def __init__(self, aPin: int):
        Pin = machine.Pin(aPin)
        W1  = onewire.OneWire(Pin)
        self.Obj = DS18X20(W1)

    def Get(self, aIDs: list) -> list:
        R = []
        if (not aIDs): 
            #Roms = W1.scan() # hangs if no devices
            aIDs = self.Obj.scan()

        self.Obj.convert_temp()
        time.sleep_ms(750)
        for ID in aIDs:
            Value = self.Obj.read_temp(ID) 
            R.append({'id':ID, 'value':Value})
        return R
