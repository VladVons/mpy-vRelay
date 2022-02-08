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
        self.Allow = []

    async def Set(self, aVal: int, aAlias: str = ''):
        if (not self.Allow) or (aAlias in self.Allow):
            return await self.Dev.Set(aVal)

    async def Get(self):
        return await self.Dev.Get()
