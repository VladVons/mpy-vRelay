'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.02.17
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
'''

import json
#
from Inc.Util import UFS, UStr


def QueryToDict(aQuery: str) -> dict:
    R = {}
    for i in aQuery.split('&'):
        Key, Value = UStr.SplitPad(2, i, '=')
        R[Key] = Value
    return R

async def QueryUrl(aPath: str, aQuery: dict) -> str:
    DirCore = 'Inc/Api'
    DirUser = 'Plugin/Api'

    Name, Ext = UStr.SplitPad(2, aPath.split('/')[-1], '.')
    if (Ext == 'py'):
        if (UFS.FileExists(DirUser + aPath)):
            Dir = DirUser
        else:
            Dir = DirCore
        Lib = __import__(Dir + '/' + Name)
        R = await Lib.TApi().Query(aQuery)
        return json.dumps(R) + '\r\n'
