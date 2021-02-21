'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.27
License:     GNU, see LICENSE for more details
Description:.
'''

import time

'''
def TimeInRange(aStart, aEnd, aX):
    if (aStart <= aEnd):
        return (aStart <= aX <= aEnd)
    else:
        return (aStart <= aX) or (aX <= aEnd)
'''

def SetTime(aTZone):
    from machine import RTC
    from ntptime import settime

    try:
        settime()
        Time = time.time() + (aTZone * 3600)
        (year, month, day, hour, minute, second, weekday, yearday) = time.localtime(Time)
        rtc  = RTC()
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
    except: pass

def GetDate():
    lt = time.localtime(time.time())
    R = '%d-%02d-%02d' % (lt[0], lt[1], lt[2])
    return R

def GetTime():
    lt = time.localtime(time.time())
    R = '%02d:%02d:%02d' % (lt[3], lt[4], lt[5])
    return R
