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


class TConnSTA(TWLan):
    def __init__(self):
        self.Event = asyncio.Event()
        self.IF = WLAN(STA_IF)

    def Mac(self):
        return GetMac(self.IF)

    async def Run(self, aSleep: int = 5):
        while True:
            if (not self.IF.isconnected()):
                await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
                await asyncio.sleep(1)

            if (self.IF.isconnected()):
                self.Event.set()
                SetTime(Conf.get('TZone', 0))
            else:
                self.Event.clear()

            await asyncio.sleep(aSleep)
