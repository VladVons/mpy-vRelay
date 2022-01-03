'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.12.22
License:     GNU, see LICENSE for more details
Description:
'''


from IncP.Dev.Gpio import GpioW


class TGpioW():
    def __init__(self, aPin):
        self.Dev = GpioW(aPin)

    async def Set(self, aVal: int):
        return await self.Dev.Set(aVal)

    async def Get(self):
        return await self.Dev.Get()
