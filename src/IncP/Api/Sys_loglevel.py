'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:
'''

from Inc.Log import Log
from IncP.Api import TApiBase


class TApi(TApiBase):
    Param = {
        'level': 1
    }

    async def Exec(self, aLevel: int) -> dict:
        R = {'old': Log.Level, 'new': aLevel}
        Log.Level = aLevel
        return R

    async def Query(self, aData: dict) -> dict:
        return await self.ExecDef(aData, ['level'])
