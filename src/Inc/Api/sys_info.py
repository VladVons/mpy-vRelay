'''
Author:      Vladimir Vons, Oster Inc.
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import gc
import os
import sys
import time
import network
#
from Inc.Conf import Conf
from Inc.NetWLan import GetMac
from Inc.Util import UTime
from Inc.Api import TApiBase

__version__ = '1.0.16 2021.01.20'
__author__  = 'Vladimir Vons, vladvons@gmail.com'


class TApi(TApiBase):
    def Exec(self) -> dict:
        gc.collect()
        Net = network.WLAN(network.STA_IF)

        R = {
            'Author':   __author__,
            'SW':       __version__,
            'FW':       os.uname().version,
            'PW':       '%s.%s.%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]),
            'Alias':    Conf.Alias,
            'Descr':    Conf.Descr,
            'MemFree':  gc.mem_free(),
            'MemAlloc': gc.mem_alloc(),
            'MAC':      GetMac(Net),
            'IP4':      Net.ifconfig(),
            'Date':     UTime.GetDate(),
            'Uptime':   int(time.ticks_ms() / 1000)
        }
        return R

    def Query(self, aData: dict) -> dict:
        return self.Exec()
