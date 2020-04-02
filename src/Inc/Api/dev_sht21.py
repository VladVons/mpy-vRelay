'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.02.11
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             SHT31 temperature-humidity sensor
'''

import machine
#
from Inc.Log import Log
from Inc.Dev.sht21 import SHT21
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Exec(self, aScl: int, aSda: int) -> dict:
        i2c = machine.I2C(scl = machine.Pin(aScl), sda = machine.Pin(aSda))
        #try:
        Obj = SHT21(i2c)
        R = [Obj.ReadTemper(), Obj.ReadHumid()]
        #except Exception as E:
        #    R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    def Query(self, aData: dict) -> dict:
        aScl = int(aData.get('scl', '5'))
        aSda = int(aData.get('sda', '4'))
        return self.Exec(aScl, aSda)