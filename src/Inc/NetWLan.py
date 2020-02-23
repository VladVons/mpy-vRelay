'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2017.02.04
License:     GNU, see LICENSE for more details
Description: 
'''

import network
import time
import ubinascii
import sys
#
from Inc.Log import Log


def GetMac(aObj) -> str:
    MacBin = aObj.config('mac')
    return ubinascii.hexlify(MacBin).decode('utf-8')


def SetAP(aESSID: str, aPassw: str):
    Obj  = network.WLAN(network.AP_IF)
    Obj.active(False)
    #MacHex = GetMac(Obj)
    #ESSID  = '%s-%s' % (aESSID, MacHex[-4:])
    #Obj.config(essid=ESSID, authmode=network.AUTH_WPA_WPA2_PSK, password=aPassw)
    #print('ESSID:', ESSID, 'Passw-8:', aPassw)
    #print('Network', Obj.ifconfig())

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


def Connect(aESSID: str, aPassw: str):
    Log.Print(1, 'Connect ESSID %s, passw %s' % (aESSID, aPassw))

    Cnt = 20
    Obj = network.WLAN(network.STA_IF)
    while (not Obj.isconnected()) and (Cnt > 0):
        Cnt -= 1
        sys.stdout.write('.')
        time.sleep(1)
    print('Network', Obj.ifconfig())
    print('MAC:', GetMac(Obj))
