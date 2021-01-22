'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.03.22
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             am2320 temperature-humidity sensor
'''

import machine
#
from Inc.Dev.bme280 import AM2320
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    def Exec(self, aScl: int, aSda: int) -> dict:
        i2c = machine.I2C(scl= machine.Pin(aScl), sda= machine.Pin(aSa))
        try:
            Obj = AM2320(i2c)
            #Obj.measure()
            #R = [Obj.temperature(), Obj.humidity()]
            R = [Obj.temperature, Obj.relative_humidity]
        except Exception as E:
            Log.Print(1, 'Err: dev_am2320', 'Api()', E)
            R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    def Query(self, aData: dict) -> dict:
        aScl = int(aData.get('scl', '5'))
        aSda = int(aData.get('sda', '4'))
        return self.Exec(aScl, aSda)
