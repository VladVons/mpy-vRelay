'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.24
License:     GNU, see LICENSE for more details
Description:.
'''


def DeepSleep(aSec: int):
    import machine

    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, aSec * 1000)
    machine.deepsleep()
