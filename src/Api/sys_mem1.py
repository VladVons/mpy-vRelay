'''
Author:      Vladimir Vons, Oster Inc.
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import gc
import time
#
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Query(self, aData: dict) -> dict:
        gc.collect()

        R = {
            'MemFree':  gc.mem_free(),
            'Uptime':    int(time.ticks_ms() / 1000)
        }
        return R
