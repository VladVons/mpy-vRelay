'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.15
License:     GNU, see LICENSE for more details
Description:
https://github.com/kipe/pycron

Minute  Hour    DOM     Month   DOW
*       8-20    *       *       *

IsNow('* 6,7,8-20 * * *')
'''


import time

def _Parse(aValue: str, aTarget: int) -> bool:
    if (aValue == '*'):
        return True

    for Value in aValue.split(','):
        if ('-' in Value):
            Start, End = Value.split('-')
            if (aTarget in range(int(Start), int(End) + 1)):
                return True
        elif (aTarget == int(Value)):
            return True
    return False

def IsNow(aPattern: str) -> bool:
    lt = time.localtime(time.time())
    Minute, Hour, DOM, Month, DOW = aPattern.split(' ')
    R = _Parse(Minute, lt[4]) and \
        _Parse(Hour, lt[3]) and \
        _Parse(DOM, lt[2]) and \
        _Parse(Month, lt[1]) and \
        _Parse(DOW, lt[6])
    return R
