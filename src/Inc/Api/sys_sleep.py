'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import time
import uasyncio as asyncio
#
from Inc.Api import TApiBase
from Inc.Log import Log

Lock = asyncio.Lock()

class TApi(TApiBase):
    Param = {
        'delay': 1, 
        'async': True,
        'echo': True
    }

    async def Exec(self, aDelay: float, aAsync: bool) -> dict:
        async with Lock:
            if (aAsync):
                await asyncio.sleep(aDelay)
            else:
                time.sleep(aDelay)
        return {'delay': aDelay, 'async': aAsync}

    async def Query(self, aData: dict) -> dict:
        R = await self.Exec(self.Get(aData, 'delay'), self.Get(aData, 'async'))
        if (self.Get(aData, 'echo')):
            Log.Print(1, 'i', 'Query()', R)
        return R
