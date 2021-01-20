'''
Copyright:   (c) 2017, Vladimir Vons, UA
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.26
License:     GNU, see LICENSE for more details
'''

import machine
import time
import os


class TSerial():
    def __init__(self, aPort: int, aSpeed: int):
        # diasable terminal echo to uart
        os.dupterm(None, aPort)

        self.uart = machine.UART(aPort)
        self.uart.init(9600, timeout = 1000)

    def Send(self, aData, aRcvLen):
        try:
            self.uart.write(aData)
            time.sleep(0.2)
            Data = self.uart.read(aRcvLen)
        except:
            Data = None

        if not (Data and len(Data) == aRcvLen and self.IsCheckSum(Data)):
            Data = None
        return Data

    def IsCheckSum(self, aData):
        pass

