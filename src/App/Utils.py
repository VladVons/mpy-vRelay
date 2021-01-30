'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.30
License:     GNU, see LICENSE for more details
Description:.
'''


import time
import uasyncio as asyncio
#
from Inc.Log  import Log
from Inc.Conf import Conf
from Inc.NetWLan import TWLan
from Inc.Util import UHrd


async def Reset(aSec: int = 0):
    from Inc.Task import Tasks

    Log.Print(1, 'i', 'Reset', aSec)
    await UHrd.ALedFlash(2, 3, 0.2)
    Tasks.Stop()
    UHrd.Reset(aSec)


class TWLanApp(TWLan):
    async def TryConnect(self):
        await self.EnableAP(False)

        Net = await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
        if (not Net.isconnected()):
            await self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, None)
            if (Net.isconnected()):
                Conf['STA_Net'] = Net.ifconfig()
                Conf.Save()
            else:
                Reset(0)
        Log.Print(1, 'i', 'TryConnect', Net.ifconfig())
        return Net.isconnected()
