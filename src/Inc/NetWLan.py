'''
Author:      Vladimir Vons, Oster Inc.
Created:     2017.02.04
License:     GNU, see LICENSE for more details
Description: 
'''

from network   import WLAN, STA_IF, AP_IF
from sys       import stdout
from time      import sleep
from machine   import idle
from ubinascii import hexlify
#
from .Log import Log


def GetMac(aObj) -> str:
    MacBin = aObj.config('mac')
    return hexlify(MacBin).decode('utf-8')


def EnableAP(aMode: bool):
    Log.Print(1, 'i', 'EnableAP %s' % aMode)

    R = WLAN(AP_IF)
    R.active(False)
    if (aMode):
        while (not R.active()):
            stdout.write('.')
            R.active(aMode)
            sleep(0.5)
    return R


def ConnectWait(aObj: WLAN, aCnt: int):
    while (not aObj.isconnected()) and (aCnt > 0):
        idle()
        stdout.write('.')
        sleep(0.5)
        aCnt -= 1
    return aCnt > 0


def Connect(aESSID: str, aPassw: str, aAddr: tuple = None, aCnt = 10) -> WLAN:
    Log.Print(1, 'i', 'Connect %s, %s, %s' % (aESSID, aPassw, aAddr))

    R = WLAN(STA_IF)
    R.active(True)
    if (aAddr):
        R.ifconfig(aAddr)
    R.connect(aESSID, aPassw)
    ConnectWait(R, aCnt)
    return R
