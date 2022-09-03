'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:
'''


import os
#
from IncP.Api import TApiBase
from Inc.Util.UFS import IsDir


class TApi(TApiBase):
    Param = {
        'path': '/'
    }

    async def Exec(self, aPath: str) -> dict:
        File = []
        Dir = []
        Files = sorted(os.listdir(aPath))
        for x in Files:
            Path = aPath + '/' + x
            if (IsDir(Path)):
                Dir.append(Path)
            else:
                File.append(Path)
        return {'dir': Dir, 'file': File}

    async def Query(self, aData: dict) -> dict:
        return await self.ExecDef(aData, ['path'])
