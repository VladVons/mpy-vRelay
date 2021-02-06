'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.30
License:     GNU, see LICENSE for more details
Description:.
'''


import time
import network
import uasyncio as asyncio
#
from Inc.Log  import Log
from Inc.Conf import Conf
from Inc.WLan import TWLan
from Inc.Util import UHrd


async def Reset(aSec: int = 0):
    from Inc.Task import Tasks

    Log.Print(1, 'i', 'Reset', aSec)
    await UHrd.ALedFlash(2, 3, 0.2)
    Tasks.Stop()
    UHrd.Reset(aSec)


class TWLanApp(TWLan):
    async def TryConnect(self, aCnt: int = 3) -> bool:
        await self.EnableAP(False)

        for Cnt in range(aCnt):
            Net = await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
            if (Net.isconnected()):
                return True
            else:
                Net.disconnect()
                await asyncio.sleep(Cnt * 2)
        await Reset(0)

    async def CheckConnect(self):
        Net = network.WLAN(network.STA_IF)
        Host = Conf.get('WatchHost', Net.ifconfig()[2]) # or gateway

        from Inc.Util.UHttp import CheckHost
        if (not await CheckHost(Host, 80, 5)):
            Log.Print(1, 'i', 'CheckConnect')
            await self.TryConnect()
