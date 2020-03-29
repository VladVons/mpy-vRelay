'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.18
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DHT22 temperature-humidity sensor
'''
import time
import machine
import onewire
import ubinascii
#
from ds18x20 import DS18X20


def Get(aPin, aID):
    Pin = machine.Pin(aPin)
    W1  = onewire.OneWire(Pin)
    Obj = DS18X20(W1)

    R = []
    if (not aID): 
        #Roms = W1.scan() # hangs if no devices
        aID = Obj.scan()

    Obj.convert_temp()
    time.sleep_ms(750)
    for ID in aID:
        Value = Obj.read_temp(ID) 
        R.append(Value)
    return R


def Api(aData: dict) -> dict:
    aPin = aData.get('pin', 0)

    HexID = []
    for ID in aData.get('id', []):
        HexID.append(ubinascii.unhexlify(ID))

    R = Get(aPin, HexID)
    return {'temperature': R}
