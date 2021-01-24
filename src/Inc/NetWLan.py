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
    R.active(aMode)
    if (aMode):
        while (not R.active()):
            stdout.write('.')
            R.active(aMode)
            sleep(0.5)
    return R


class TWLan():
    Cnt = 10

    def _Wait(self):
        Cnt = self.Cnt
        while (not self.Net.isconnected()) and (Cnt > 0):
            idle()
            stdout.write('.')
            self.DoWait()
            Cnt -= 1
        return Cnt > 0

    def Connect(self, aESSID: str, aPassw: str, aAddr: tuple = None):
        Log.Print(1, 'i', 'Connect %s, %s, %s' % (aESSID, aPassw, aAddr))

        Net = WLAN(STA_IF)
        self.Net = Net

        Net.active(True)
        if (aAddr):
            Net.ifconfig(aAddr)
        Net.connect(aESSID, aPassw)
        self._Wait()

    def DoWait(self):
        sleep(0.5)
