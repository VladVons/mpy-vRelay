'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


from .Dev import TDev
from IncP.Dev.dht22 import DHT22


class TDevDT(TDev):
    def __init__(self, aPin):
        super().__init__(0.5, 10)
        self.Dev = DHT22(aPin)

    async def Read(self):
        R = await self.Dev.Get()
        return R[0]

'''
class TDevDH(TDev):
    def __init__(self, aPin):
        super().__init__(0.5, 10)
        self.Dev = DHT22(aPin)

    async def Read(self):
        R = await self.Dev.Get()
        return R[1]
'''
