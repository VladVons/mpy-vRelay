'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.01.12
License:     GNU, see LICENSE for more details
Description:
'''

import json
import uasyncio as asyncio
#
from App import ConfApp
from IncP.BLE import TBLE
from Inc.Log  import Log
from Inc.Plugin import Plugin
from Inc.Sender import TSender


class TBleEx(TBLE):
    def _DoReceive(self, aMsg: str):
        print('DoReceive', aMsg)

    async def Run(self, aSleep: int = 3):
        Cnt = 0
        while True:
            Cnt += 1
            Msg = "Hello %s" % (Cnt)
            self.Send(Msg)
            await asyncio.sleep(aSleep)
