'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.03.04
License:     GNU, see LICENSE for more details
Description:
'''


import time
#
from Inc.Log import Log


class TSen():
    ValD = 1.0
    SecD = 60
    Val  = 0
    Time = 0

    async def Check(self) -> bool:
        try:
            Val = await self.Get()
            Res = (Val is not None) and (abs(Val - self.Val) > self.ValD) or (time.time() - self.Time > self.SecD)
            if (Res):
                self.Time = time.time()
            self.Val = Val
            return Res
        except Exception as E:
            Log.Print(1, 'x', 'Check()', E)

    def Info(self) -> dict:
        return {'Val': self.Val, 'Owner': self.__class__.__name__, 'Alias': self.Alias}
