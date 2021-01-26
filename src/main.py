'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''

import time
import gc


def Run():
    gc.collect()
    print()
    print('MemFree boot', gc.mem_free())

    from App import Main

    print('MemFree App', gc.mem_free())

    print('sleep 0.1')
    time.sleep(0.1)

    Main.Run()


Run()
#import Test

