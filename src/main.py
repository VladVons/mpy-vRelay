'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:
'''

import time, gc, esp


'''
def RecursLimit(aCnt: int) -> int:
    # mptask.h, MICROPY_TASK_STACK_SIZE
    try:
        return RecursLimit(aCnt + 1)
    except:
        return aCnt

print('Recursion limit', RecursLimit(0))
'''

esp.osdebug(None)

gc.collect()
print()
print('MemFree boot', gc.mem_free())

from App.Main import Run
import uasyncio as asyncio

Wait = 0.1
print('sleep', Wait)
time.sleep(Wait)

asyncio.run(Run())

print('End')
