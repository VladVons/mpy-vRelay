'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description: 
'''

import time, gc, esp 


def RecursLimit(aCnt: int) -> int:
    # mptask.h, MICROPY_TASK_STACK_SIZE
    try:
        return RecursLimit(aCnt + 1)
    except:
        return aCnt

def Main():
    esp.osdebug(None)

    gc.collect()
    print()
    print('MemFree boot', gc.mem_free())

    from App import Main
    gc.collect()
    print('MemFree App', gc.mem_free())

    print('sleep 0.1')
    time.sleep(0.1)

    Main.Main()


def Test1():
    import time
    from IncP.BLE import TBLE
    BLE = TBLE('MyBLE')
    Cnt = 0
    while True:
        Cnt += 1
        Msg = "Hello %s" % (Cnt)
        BLE.Write(Msg)
        time.sleep(2)

Test1()

#import Test3
#print('Recursion limit', RecursLimit(0))

#Main()
#print('End')

