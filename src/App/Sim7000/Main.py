'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.23
License:     GNU, see LICENSE for more details
Description:.

https://github.com/tmcadam/sim7000-tools/blob/master/sim7000.py
https://github.com/search?l=Python&q=sim7000&type=Repositories

https://simcom.ee/documents/?dir=SIM7000x
https://m2msupport.net/m2msupport/tutorial-for-simcom-m2m-modules/#Network
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

        #self.Event = asyncio.Event()

    @staticmethod
    async def SetPower(aOn: bool, aPin: int = 4):
        Obj = Pin(aPin, Pin.OUT)
        Obj.value(aOn)
        await asyncio.sleep(2)

    async def AT(self, aCmd, aSleep = 0.1):
        #Log.Print(1, 'i', 'AT', aCmd)

        self.SW.write(('AT' + aCmd + '\r\n').encode('utf-8'))
        await self.SW.drain()
        await asyncio.sleep(aSleep)

    '''
    # ToDo. unstable. Perhapse ReadWrite as follow
    #with UART(PORT, BAUD, timeout=1) as ser:
    async def Send(self, aCmd: str, aSleep = 0.1):
        self.Event.clear() # stop Reader()
        await self.AT(aCmd, aSleep)
        try:
            R = await asyncio.wait_for(self.Read(), timeout=3)
        except:
            R = None
        self.Event.set()
        return R
    '''

    async def DoRead(self, aCmd, aRes, aErr):
        Log.Print(1, 'i', 'Handle', aCmd, aRes, aErr)

        if (aCmd == 'AT+CGNSINF'):
            #+CGNSINF: 1,1,20210224133650.000,49.550612,25.592956,334.900,0.00,323.3,1,,2.8,2.9,1.0,,11,3,,,38,,
            #Date, Lat, Lon, Alt, Speed = aRes.split(',')[2:7]
            pass

    async def Read(self, aBreak = ['OK','ERROR']):
        Cmd = Res = ''
        for i in range(5):
            try:
                Line = await self.SR.readline()
                Line = Line.decode('utf-8').strip()
            except Exception as E:
                return

            #Log.Print(1, 'i', 'Read', Line)
            if (Line.startswith('AT')):
                Cmd = Line
            elif (Line in aBreak):
                return (Cmd, Res, Line)
            elif (Line != ''):
                Res = Line

    async def Reader(self):
        #self.Event.set()
        while True:
            #await self.Event.wait()
            Data = await self.Read()
            if (Data):
                await self.DoRead(*Data)

    async def Run(self, aSleep: int = 5):
        await self.SetPower(True)

        asyncio.create_task(self.Reader())

        while True:
            await self.AT('') # ToDo. readline hangs without it

            await self.AT("+CGMI") # manufacturer
            #await self.AT("+CGMM") # Module name

            await self.AT('+CGNSPWR=1') # Power on and wait 2s
            await self.AT('+CGNSINF')
            #await self.AT('+CGNSPWR=0', 3) # Power off

            await asyncio.sleep(aSleep)
