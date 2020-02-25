'''
Author:      Vladimir Vons <VladVons@gmail.com>, Oster Inc
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''


def GetAttr(aO, aName: str):
    R = None
    if (hasattr(aO, aName)):
        R = getattr(aO, aName)
    return R
