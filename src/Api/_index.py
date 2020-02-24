'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import gc
import os
import sys
import time
#
from Conf import Conf

__version__ = '1.0.15'


def GetMac():
    import network
    import ubinascii

    Obj    = network.WLAN(network.AP_IF)
    MacBin = Obj.config('mac')
    return ubinascii.hexlify(MacBin).decode('utf-8')


def Api(aData):
    gc.collect()

    R = {
        'Author':  'VladVons@gmail.com',
        'SW':      __version__,
        'FW':       os.uname().version,
        'PW':       '%s.%s.%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]),
        'ID':       Conf.Get('ID'),
        'MemFree':  gc.mem_free(),
        'MemAlloc': gc.mem_alloc(),
        'MAC':      GetMac(),
        'Uptime':   int(time.ticks_ms() / 1000)
    }
    return R
