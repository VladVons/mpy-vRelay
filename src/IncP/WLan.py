'''
Author:      Vladimir Vons, Oster Inc.
Created:     2017.02.04
License:     GNU, see LICENSE for more details
Description:
'''


from network   import WLAN, STA_IF, AP_IF, AUTH_WPA_WPA2_PSK
from sys       import stdout, platform
from machine   import idle
from ubinascii import hexlify
from uasyncio  import sleep
#
from IncP.Log import Log


def GetMac(aObj) -> str:
    MacBin = aObj.config('mac')
    return hexlify(MacBin).decode('utf-8')


class TWLan():
    Cnt = 10
    Delay = 1

    async def _WaitForReady(self, aFunc) -> bool:
        Cnt = self.Cnt
        while (not aFunc()) and (Cnt > 0):
            idle()
            stdout.write('.')
            await sleep(self.Delay)
            Cnt -= 1
        return Cnt > 0

    async def Connect(self, aESSID: str, aPassw: str, aAddr: tuple = None):
        Log.Print(1, 'i', 'Connect() %s, %s, %s' % (aESSID, aPassw, aAddr))

        # Improve connection integrity at cost of power consumption
        if (platform == 'esp8266'):
            from esp import sleep_type
            sleep_type(0)

        R = WLAN(STA_IF)
        R.active(False)
        await sleep(1)
        R.active(True)

        if (aAddr):
            R.ifconfig(aAddr)

        R.connect(aESSID, aPassw)
        await self._WaitForReady(R.isconnected)

        Log.Print(1, 'i', 'Net', R.ifconfig())
        return R

    async def EnableAP(self, aMode: bool, aPassw = None):
        Log.Print(1, 'i', 'EnableAP() %s, %s ' % (aMode, aPassw))

        R = WLAN(AP_IF)
        R.active(False)
        await sleep(1)
        R.active(aMode)

        if (aMode):
            R.config(essid='vRelay-' + GetMac(R)[-4:], authmode=AUTH_WPA_WPA2_PSK, password=aPassw)
            await self._WaitForReady(R.active)
        return R
