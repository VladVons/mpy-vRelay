'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.27
License:     GNU, see LICENSE for more details
Description:
'''

import time

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
