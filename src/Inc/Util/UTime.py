'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.27
License:     GNU, see LICENSE for more details
Description:.
'''

import time


def SetTime(aTZone):
    import machine
    from ntptime import settime

    try:
        settime()
        Time = time.time() + (aTZone * 3600) 
        (year, month, day, hour, minute, second, weekday, yearday) = time.localtime(Time)
        rtc  = machine.RTC()
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
    except: pass


def GetDate():
    lt = time.localtime(time.time())
    Now = '%d-%02d-%02d,%02d:%02d:%02d' % (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])
    return Now
 