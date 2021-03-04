'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


import time


class TDev():
    def __init__(self, aValD: float, aSecD: int = 60):
        self.ValD = aValD
        self.SecD = aSecD
        self.Val = 0
        self.Time = 0

    async def Check(self):
        Val = await self.Read()
        if (Val is not None):
            if (abs(Val - self.Val) > self.ValD) or (time.time() - self.Time > self.SecD):
                self.Time = time.time()
                self.Val = Val
                return True

    def Info(self):
        return [self.Val, self.__class__.__name__, self.Time]


    '''
    def Read(self):
        pass
    '''
