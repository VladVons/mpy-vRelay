'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


from .Dev import TDev
from IncP.Dev.emu_cycle import TCycle


class TDevCycle(TDev):
    def __init__(self, aStart: int, aEnd: int):
        super().__init__(0.5, 10)
        self.Dev = TCycle(aStart, aEnd)

    async def Read(self):
        R = await self.Dev.Get()
        return R[0]
