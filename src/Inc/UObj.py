'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''


def GetAttr(aObj, aName: str):
    R = None
    if (hasattr(aObj, aName)):
        R = getattr(aObj, aName)
    return R
