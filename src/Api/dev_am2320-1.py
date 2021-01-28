'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.03.22
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             am2320 temperature-humidity sensor
'''

import machine
import sys
#
#from Inc.Dev.am2320 import AM2320
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    async def Exec(self, aScl: int, aSda: int) -> dict:
        i2c = machine.I2C(scl=machine.Pin(aScl), sda=machine.Pin(aSda))
        try:
            Obj = AM2320(i2c)
            await Obj.measure()
            R = [Obj.temperature(), Obj.humidity()]
        except Exception as E:
            Log.Print(1, 'x', 'dev_am2320', E)
            R = [None, None]
        return {'temperature': R[0], 'humidity': R[1]}

    async def Query(self, aData: dict) -> dict:
        aScl = int(aData.get('scl', '5'))
        aSda = int(aData.get('sda', '4'))
        return await self.Exec(aScl, aSda)


import ustruct
import time
import uasyncio as asyncio

Lock = asyncio.Lock()

class AM2320:
    def __init__(self, i2c=None, address=0x5c):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(8)

    async def measure(self):
        buf = self.buf
        address = self.address

        async with Lock:
            # wake sensor
            try:
                self.i2c.writeto(address, b'')
            except OSError:
                print('Except OSError')

            await asyncio.sleep_ms(10)
            # read 4 registers starting at offset 0x00
            self.i2c.writeto(address, b'\x03\x00\x04')
            # wait at least 1.5ms
            await asyncio.sleep_ms(2)
            # read data
            self.i2c.readfrom_mem_into(address, 0, buf)
            crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]
            if (crc != self.crc16(buf[:-2])):
                raise Exception("checksum error")

    def crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if (crc & 0x01):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def humidity(self):
        return (self.buf[2] << 8 | self.buf[3]) * 0.1

    def temperature(self):
        t = ((self.buf[4] & 0x7f) << 8 | self.buf[5]) * 0.1
        if (self.buf[4] & 0x80):
            t = -t
        return t
