'''
Author:      Vladimir Vons, Oster Inc.
Created:     2017.02.04
License:     GNU, see LICENSE for more details
Description: 
'''

import network
import time
import ubinascii
import sys
#
from .Log import Log


def GetMac(aObj) -> str:
    MacBin = aObj.config('mac')
    return ubinascii.hexlify(MacBin).decode('utf-8')


def EnableAP(aMode: bool):
    Log.Print(1, 'EnableAP %s' % aMode)

    R = network.WLAN(network.AP_IF)
    R.active(False)
    if (aMode):
        while (not R.active()):
            sys.stdout.write('.')
            R.active(True)
            time.sleep(1)
    return R


def ConnectWait(aObj, aCnt: int):
    while (not aObj.isconnected()) and (aCnt > 0):
        sys.stdout.write('.')
        time.sleep(1)
        aCnt -= 1
    return aCnt > 0


def ConnectDhcp(aESSID: str, aPassw: str, aCnt: int = 20) -> bool:
    Log.Print(1, 'Connect ESSID `%s`, Passw `%s`' % (aESSID, aPassw))

    Obj = network.WLAN(network.STA_IF)
    if (not Obj.isconnected()):
        Obj.active(True)
        Obj.connect(aESSID, aPassw)
        ConnectWait(Obj, aCnt)
    print('MAC:', GetMac(Obj))
    print('Network', Obj.ifconfig())
    return Obj


def ConnectStat(aESSID: str, aPassw: str, aAddr: tuple) -> bool:
    Log.Print(1, 'Connect ESSID `%s`, Passw `%s`, %s' % (aESSID, aPassw, aAddr))
    Obj = network.WLAN(network.STA_IF)
    Obj.active(True)
    Obj.ifconfig(aAddr)
    Obj.connect(aESSID, aPassw)
    ConnectWait(Obj, 10)
    return Obj
