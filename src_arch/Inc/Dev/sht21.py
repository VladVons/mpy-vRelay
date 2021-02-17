'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.04.01
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             SHT21 temperature-humidity sensor
'''


from machine import I2C
import time


class SHT21():
    _ADDR   = 0x40
    _RESET  = b'\xFE'
    _TEMPER = b'\xF3'
    _HUMID  = b'\xF5'

    def __init__(self, ai2c):
        self.i2c = ai2c
        self.i2c.writeto(self._ADDR, self._RESET)
        time.sleep_ms(15)

    def GetCrc(self, aBuf: bytearray) -> int:
        R = 0
        for Val in aBuf:
            R ^= Val
            for _ in range(8, 0, -1):
                if (R & 0x80):
                    R = (R << 1) ^ 0x131   #P(x)=x^8+x^5+x^4+1 = 100110001
                else:
                    R = (R << 1)
        return R

    def ReadTemper(self):    
        self.i2c.writeto(self._ADDR, self._TEMPER)
        time.sleep_ms(250)

        Data = self.i2c.readfrom(self._ADDR, 3)
        if (self.GetCrc(Data[:2]) == Data[2]):
            R = (Data[0] << 8) + Data[1]
            R *= 175.72
            R /= 1 << 16
            R -= 46.85
            return R

    def ReadHumid(self):    
        self.i2c.writeto(self._ADDR, self._HUMID)
        time.sleep_ms(250)

        Data = self.i2c.readfrom(self._ADDR, 3)
        if (self.GetCrc(Data[:2]) == Data[2]):
            R = (Data[0] << 8) + Data[1]
            R *= 125
            R /= 1 << 16
            R -= 6
            return R
