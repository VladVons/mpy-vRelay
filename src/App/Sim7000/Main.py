'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.23
License:     GNU, see LICENSE for more details
Description:.

https://github.com/tmcadam/sim7000-tools/blob/master/sim7000.py
'''


import uasyncio as asyncio
from machine import UART, Pin
#
from Inc.Log import Log


class TSim7000():
    def __init__(self, aPort: int = 1, aRx: int = 26, aTx: int = 27):
        Uart = UART(aPort, baudrate=9600, bits=8, parity=None, stop=1, rx=aRx, tx=aTx)
        self.SR = asyncio.StreamReader(Uart)
        self.SW = asyncio.StreamWriter(Uart)

    @staticmethod
    async def SetPower(aOn: bool, aPin: int = 4):
        Obj = Pin(aPin, Pin.OUT)
        Obj.value(aOn)
        await asyncio.sleep(1.5)

    async def AT(self, aCmd, aSleep = 0.1):
        Log.Print(1, 'i', 'AT', aCmd)

        self.SW.write(('AT' + aCmd + '\r\n').encode('utf-8'))
        await self.SW.drain()
        await asyncio.sleep(aSleep)

    async def Reader(self):
        while True:
            Line = await self.SR.readline()
            Log.Print(1, 'i', 'Reader', Line)

    async def Run(self, aSleep: int = 5):
        self.SetPower(True)

        asyncio.create_task(self.Reader())

        await self.AT('')
        await self.AT("+CGMM") # Module name
        await self.AT("+CGMR") # Firmware version
        await self.AT('+CGNSPWR=1', 2) # Power on

        while True:
            await self.AT('+CGNSINF')
            #await self.AT('+CGNSPWR=0', 3) # Power off
            await asyncio.sleep(aSleep)
