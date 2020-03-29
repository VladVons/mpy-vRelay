'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.17
License:     GNU, see LICENSE for more details
Description:.
'''

import json
#
from machine import Pin


def Api(aData: dict) -> dict:
    for Key, Val in aData.items():
        Obj = Pin(int(Key), Pin.OUT)
        Obj.value(int(Val))
