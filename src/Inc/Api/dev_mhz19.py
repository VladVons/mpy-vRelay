'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.04.25
License:     GNU, see LICENSE for more details
Description:
'''


from Inc.Log import Log
from Inc.Dev.mhz19 import MHZ19


def Api(aData: dict) -> dict:
    aPort  = int(aData.get('port', '1'))
    aSpeed = int(aData.get('speed', '9600'))
    try:
        Obj = MHZ19(aPort, aSpeed)
        R = Obj.GetCO2()
    except Exception as E:
        Log.Print(1, 'x', 'mhz19.Api()', E)
        R = None
    return {'co2': R}
