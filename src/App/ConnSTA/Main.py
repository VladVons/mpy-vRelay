'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.21
License:     GNU, see LICENSE for more details
Description:
'''


import uasyncio as asyncio
from network import WLAN, STA_IF
#
from App import ConfApp
from Inc.Log import Log
from Inc.Plugin import Plugin
from Inc.Util.UNet import CheckHost
from IncP.WLan import TWLan, GetMac
from IncP.Util.UTime import SetTime


class TConnSTA(TWLan):
    def __init__(self):
        self.Event = asyncio.Event()
        self.IF = WLAN(STA_IF)
        self.Last = None

    def Mac(self):
        return GetMac(self.IF)

    async def IsOk(self) -> bool:
        Host = ConfApp.get('WatchHost', self.IF.ifconfig()[2]) # or gateway
        Res = (self.IF.isconnected) and (await CheckHost(Host, 80, 3))
        return bool(Res) # (None and False) = None

    async def Post(self, aVal):
        await Plugin.Post(self, {'Val': aVal, 'Owner': self.__class__.__name__})

    async def Connector(self):
        if (not await self.IsOk()):
            try:
                await self.Connect(ConfApp.STA_ESSID, ConfApp.STA_Paswd, ConfApp.STA_Net)
            except Exception as E:
                Log.Print(1, 'x', 'Connector()', E)

        Ok = await self.IsOk()
        if (self.Last != Ok):
            self.Last = Ok
            await self.Post(int(Ok))

        if (Ok):
            self.Event.set()
            SetTime(ConfApp.get('TZone', 2))
        else:
            self.Event.clear()

    async def Run(self, aSleep: int = 60):
        await self.Post(-1)

        while True:
            await self.Connector()

            await asyncio.sleep(aSleep)
