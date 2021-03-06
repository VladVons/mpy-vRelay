'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import os


def FileLoad(aName: str, aMode: str = 'r') -> str:
    try:
        with open(aName, aMode) as F:
            R = F.read()
    except:
        R = ''
    return R

def FileStat(aName: str) -> tuple:
    try:
        R = os.stat(aName)
    except:
        R = None
    return R

def FileExists(aName: str) -> bool:
    return FileStat(aName) is not None

def FileSize(aName: str) -> int:
    return FileStat(aName)[6]
