'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from network import WLAN, STA_IF
#
from Inc.Log import Log
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.Util.UNet import CheckHost
from IncP.WLan import TWLan, GetMac
from IncP.Util.UTime import SetTime


class TConnSTA(TWLan):
    def __init__(self):
        self.Event = asyncio.Event()
        self.IF = WLAN(STA_IF)

    def Mac(self):
        return GetMac(self.IF)

    async def IsOk(self):
        Host = Conf.get('WatchHost', self.IF.ifconfig()[2]) # or gateway
        return (self.IF.isconnected) and (await CheckHost(Host, 80, 3))

    async def Post(self, aVal):
        await Plugin.Post(self, {'Val': aVal, 'Owner': self.__class__.__name__})

    async def Connector(self):
        if (not await self.IsOk()):
            await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)

        IsOk = await self.IsOk()
        if (IsOk):
            self.Event.set()
            SetTime(Conf.get('TZone', 2))
        else:
            self.Event.clear()
        await self.Post(int(IsOk))

    async def Run(self, aSleep: int = 60):
        await self.Post(-1)

        while True:
            await self.Connector()

            await asyncio.sleep(aSleep)
