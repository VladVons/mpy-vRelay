'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import os, gc
import machine
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Plugin import Plugin


async def Run():
    Log.Print(1, 'i', 'Run', os.uname())

    #DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    #print('DSleep', DSleep)

    Plugin.LoadList(Conf.get('Plugins', 'App.HttpSrv'))
    Plugin.LoadDir('Plugin/App')

    gc.collect()
    Log.Print(1, 'i', 'Run()', 'MemFree %d' % (gc.mem_free()))

    try:
        await Plugin.Run()
    except KeyboardInterrupt:
        print('Ctrl-C')
    finally:
        await Plugin.Stop()


def Main():
    asyncio.run(Run())
