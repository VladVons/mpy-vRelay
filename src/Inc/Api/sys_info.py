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
from Inc.WLan import GetMac
from Inc.Util.UTime import GetDate, GetTime

__version__ = '1.1.04, 2021.02.19'
__author__  = 'Vladimir Vons, vladvons@gmail.com'


class TApi():
    async def Exec(self) -> dict:
        gc.collect()
        NetSTA = network.WLAN(network.STA_IF)
        NetAP  = network.WLAN(network.AP_IF)

        R = {
            'Author':   __author__,
            'SoftWare': __version__,
            'FirmWare': os.uname().version,
            'Python':   '%s.%s.%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]),
            'Platform': sys.platform,
            'Descr':    '%s, %s' % (Conf.Alias, Conf.Descr),
            'MemFree':  gc.mem_free(),
            'MemAlloc': gc.mem_alloc(),
            'MAC':      GetMac(NetSTA),
            'IP STA':   NetSTA.ifconfig(),
            'IP AP':    NetAP.ifconfig(),
            'Disk':     os.statvfs('/'),
            'Date':     '%s, %s'% (GetDate(), GetTime()),
            'Uptime':   int(time.ticks_ms() / 1000)
        }
        return R

    async def Query(self, aData: dict) -> dict:
        return await self.Exec()
