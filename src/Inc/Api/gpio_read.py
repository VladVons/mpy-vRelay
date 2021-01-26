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
    async def Exec(self, aPins: list) -> dict:
        R = {}
        try:
            for PinNo in aPins:
                Obj = Pin(PinNo, Pin.IN)
                R[str(PinNo)] = Obj.value()
        except Exception as E:
            Log.Print(1, 'Err: gpio_read', 'Api()', E)
            R[str(PinNo)] = None
        return R

    async def Query(self, aData: dict) -> dict:
        aPins = aData.get('pin', '').split(',')

        Param = []
        for Pin in aPins:
            Param.append(int(Pin))
        return await self.Exec(Param)
