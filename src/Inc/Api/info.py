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


__version__ = '1.0.15'
__author__  = 'Vladimir Vons, Oster Inc.'


def Api(aData):
    gc.collect()

    R = {
        'Author':   __author__,
        'SW':       __version__,
        'FW':       os.uname().version,
        'PW':       '%s.%s.%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]),
        'Alias':    Conf.Alias,
        'MemFree':  gc.mem_free(),
        'MemAlloc': gc.mem_alloc(),
        'MAC':      GetMac(network.WLAN(network.STA_IF)),
        'Date':     UTime.GetDate(),
        'Uptime':   int(time.ticks_ms() / 1000)
    }
    return R
