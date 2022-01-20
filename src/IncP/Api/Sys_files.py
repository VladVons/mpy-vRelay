'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:
'''


import os
#
from IncP.Api import TApiBase


class TApi(TApiBase):
    Param = {
        'path': '/'
    }

    async def Exec(self, aPath: str) -> dict:
        return {'files': os.listdir(aPath)}

    async def Query(self, aData: dict) -> dict:
        return await self.ExecDef(aData, ['path'])
