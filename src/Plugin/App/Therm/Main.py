'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Plugin import Plugin
from Inc.Log  import Log
from Inc.Hyster import THyster

#from IncP.Api.dev_dht22 import TApi
from IncP.Api.emu_cycle import TApi


class TTherm():
    def __init__(self):
        self.Hyst = THyster()
        self.Val = None

    async def Read(self):
        R = await TApi().Exec(0, 15)
        Val = R['value']
        State = self.Hyst.Check(10, Val)
        #Val = await TApi().Exec(14)
        #Val = {'temperature': await TApi().Exec(20, 30)['value']}
        #if (Val['temperature'] is not None):
        #    self.Val = Val
        #    State = self.Hyst.Check(10, Val['temperature'])

    async def _DoPost(self, aOwner, aMsg):
        print('Im TTherm', aOwner, aMsg)
        return 'from TTherm'

    async def Run(self, aSleep: float = 5):
        while True:
            await self.Read()
            await asyncio.sleep(aSleep)
