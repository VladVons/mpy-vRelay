'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
#
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Exec(self) -> dict:
        machine.reset()

    def Query(self, aData: dict) -> dict:
        return self.Exec()
