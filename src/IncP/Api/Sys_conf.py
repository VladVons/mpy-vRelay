'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.02.06
License:     GNU, see LICENSE for more details
Description: 
'''

from Inc.Conf import Conf


class TApi():
    async def Exec(self) -> dict:
        return Conf.Keys()

    async def Query(self, aData: dict) -> dict:
        return await self.Exec()