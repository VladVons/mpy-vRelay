'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


from .Sen import TSen
from IncP.Dev.Sen_dht22 import DHT22


class TSen_dht22_t(TSen):
    def __init__(self, aPin):
        self.Dev = DHT22(aPin)

    async def Get(self):
        R = await self.Dev.Get()
        return R[0]


class TSen_dht22_h(TSen):
    def __init__(self, aPin):
        self.Dev = DHT22(aPin)

    async def Get(self):
        R = await self.Dev.Get()
        return R[1]
