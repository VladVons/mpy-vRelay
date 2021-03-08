'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.02.19
License:     GNU, see LICENSE for more details
Description:.
'''


import gc, os, sys, time, network, machine
from ubinascii import hexlify
#
from Inc.Conf import Conf
from Inc.Util.UTime import GetDate, GetTime
from IncP.WLan import GetMac

__version__ = '1.1.06, 2021.03.08'
__author__  = 'Vladimir Vons, vladvons@gmail.com'


class TInfo():
    async def Get(self):
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
            #'ID':       hexlify(machine.unique_id()).decode('utf-8'),
            'MAC':      GetMac(NetSTA),
            'IP STA':   NetSTA.ifconfig(),
            'IP AP':    NetAP.ifconfig(),
            'Disk':     os.statvfs('/'),
            'Date':     '%s, %s'% (GetDate(), GetTime()),
            'Uptime':   int(time.ticks_ms() / 1000)
        }
        return [0, R]
