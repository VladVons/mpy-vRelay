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
from Inc.NetWLan import TWLan, EnableAP
from Inc.Util import UHrd


async def Reset(aSec: int = 0):
    from Inc.Task import Tasks

    Log.Print(1, 'i', 'Reset', aSec)
    await UHrd.ALedFlash(2, 3, 0.2)
    Tasks.Stop()
    UHrd.Reset(aSec)


class TWLanApp(TWLan):
    def TryConnect(self):
        EnableAP(False)

        print('Press `m` to enter menu')
        self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
        if (not self.Net.isconnected()):
            self.Connect(Conf.STA_ESSID, Conf.STA_Paswd, None)
            if (self.Net.isconnected()):
                Conf['STA_Net'] = self.Net.ifconfig()
                Conf.Save()
            else:
                Reset(0)
        Log.Print(1, 'i', 'TryConnect', self.Net.ifconfig())
        return self.Net.isconnected()

    def DoWait(self):
        time.sleep(0.5)

        #Key = UHrd.GetInputChr()
        #if (Key == 'm'):
        #    from .Menu import TMenuApp
        #    Menu = TMenuApp()
        #    Menu.MMain('/Main', [])
  