'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from network import WLAN, STA_IF
#
from Inc.WLan import TWLan, GetMac
from Inc.Log import Log
from Inc.Conf import Conf
from Inc.Util.UTime import SetTime
from Inc.Util.UNet import CheckHost


class TConnSTA(TWLan):
    def __init__(self):
        self.Event = asyncio.Event()
        self.IF = WLAN(STA_IF)

    def Mac(self):
        return GetMac(self.IF)

    async def IsOk(self):
        Host = Conf.get('WatchHost', self.IF.ifconfig()[2]) # or gateway
        return (self.IF.isconnected) and (await CheckHost(Host, 80, 3))

    async def Run(self, aSleep: int = 15):
        while True:
            if (not await self.IsOk()):
                await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
                SetTime(Conf.get('TZone', 2))

            if (await self.IsOk()):
                self.Event.set()
            else:
                self.Event.clear()

            await asyncio.sleep(aSleep)
