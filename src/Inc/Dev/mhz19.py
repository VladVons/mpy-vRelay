'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.04.25
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             mhz19 CO2 sensor
'''

from Inc.Dev.Serial import TSerial


class MHZ19(TSerial):
    def IsCheckSum(self, aData):
        Sum = 0
        for i in range(1, 7):
            Sum += aData[i]
        Sum = ~Sum & 0xFF
        Sum += 1

        CheckSum = aData[-1]
        return (CheckSum == Sum)

    def GetCO2(self):
        Out = b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'
        In = self.Send(Out, 9)
        R = (In[2] * 256) + In[3]
        return R
