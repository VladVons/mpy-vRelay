'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


from .Sen import TSen
from IncP.Dev.Sen_ds18b20 import DS1820


class TSen_ds18b20(TSen):
    def __init__(self, aPin):
        self.Dev = DS1820(aPin)

    async def Get(self):
        R = await self.Dev.Get()
        return R[0]['value']
