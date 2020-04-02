'''
Author:      Vladimir Vons, Oster Inc.
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import gc
#
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Exec(self) -> dict:
        gc.collect()

        R = {
            'MemFree':  gc.mem_free(),
            'MemAlloc': gc.mem_alloc(),
        }
        return R

    def Query(self, aData: dict) -> dict:
        return self.Exec()
