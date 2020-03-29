'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''


from machine import Pin


def Api(aData: dict) -> dict:
    aPins = aData.get('pin', '')

    R = {}
    for Key in aPins.split(','):
        Obj = Pin(int(Key), Pin.IN)
        R[Key.strip()] = Obj.value()
    return R
