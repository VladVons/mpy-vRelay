'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''


def GetAttr(aO, aName: str):
    R = None
    if (hasattr(aO, aName)):
        R = getattr(aO, aName)
    return R


def GetTree(aObj, aPrefix: str = '', aDepth: int = 99):
    R = []

    Type = type(aObj).__name__
    if (aDepth > 0):
        if (Type == 'dict'):
            for Key in aObj:
                Data = GetTree(aObj[Key], aPrefix + '/' + Key, aDepth - 1)
                R.extend(Data)
        elif (Type == 'list'):
            for Obj in aObj:
                Data = GetTree(Obj, aPrefix, aDepth - 1)
                R.extend(Data)
        else:
            Data = {'Key': aPrefix, 'Val': aObj}
            R.append(Data)
    return R
