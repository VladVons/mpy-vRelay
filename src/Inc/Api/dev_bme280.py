'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             BME temperature-humidity-preasure sensor
'''

import machine
#
from Inc.Dev.bme280 import BME280
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    async def Exec(self, aScl: int, aSda: int) -> dict:
        i2c = machine.I2C(scl = machine.Pin(aScl), sda = machine.Pin(aSda), freq = 10000)
        try:
            Obj = BME280(i2c = i2c)
            R = await Obj.read_compensated_data()
        except Exception as E:
            Log.Print(1, 'x', 'dev_bme280', E)
            R = [None, None, None]
        return {'temperature': R[0], 'humidity': R[2], 'preasure': R[1]}

    async def Query(self, aData: dict) -> dict:
        aScl = int(aData.get('scl', '5'))
        aSda = int(aData.get('sda', '4'))
        return await self.Exec(aScl, aSda)
