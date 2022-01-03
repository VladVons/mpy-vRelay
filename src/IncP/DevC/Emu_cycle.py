'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


from .Sen import TSen
from IncP.Dev.Emu_cycle import TCycle


class TEmu_cycle(TSen):
    def __init__(self, aStart: int, aEnd: int):
        self.Dev = TCycle(aStart, aEnd)

    async def Get(self):
        R = await self.Dev.Get()
        return R[0]

    def Get2(self):
        return [self.Dev.Start, self.Dev.End]