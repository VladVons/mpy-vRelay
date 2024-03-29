'''
Author:      Vladimir Vons, Oster Inc.
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:
'''


import gc, time
import uasyncio as asyncio
#
from IncP.Api import TApiBase


class TApi(TApiBase):
    async def Query(self, aData: dict) -> dict:
        gc.collect()

        R = {
            'MemFree':  gc.mem_free(),
            'Uptime':   int(time.ticks_ms() / 1000)
        }

        return R
