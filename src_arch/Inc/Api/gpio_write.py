'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

from machine import Pin
#
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    async def Exec(self, aPairs: list) -> dict:
        R = {}
        try:
            for PinNo, Val in aPairs:
                Obj = Pin(PinNo, Pin.OUT)
                Obj.value(Val)
                R[str(PinNo)] = Obj.value()
        except Exception as E:
            Log.Print(1, 'x', 'gpio_write', E)
            R[str(PinNo)] = None
        return R

    async def Query(self, aData: dict) -> dict:
        Pairs = []
        for Key, Val in aData.items():
            Pairs.append([int(Key), int(Val)])
        return await self.Exec(Pairs)
