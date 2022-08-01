'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:
'''


import os, gc
import machine
#
from . import ConfApp
from IncP.Log import Log, TEchoConsoleEx
from Inc.Plugin import Plugin


async def Run():
    Log.AddEcho(TEchoConsoleEx())
    Log.Print(1, 'i', 'Run', os.uname())

    #DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    #print('DSleep', DSleep)

    Plugin.LoadList(ConfApp.get('Plugins', 'App.HttpSrv'), ConfApp.get('PluginsSkip', ''))
    Plugin.LoadDir('Plugin/App')
    #Plugins = sorted(list(Plugin.keys()))
    #print('Plugins', Plugins)

    gc.collect()
    Log.Print(1, 'i', 'Run()', 'MemFree %d' % (gc.mem_free()))

    try:
        await Plugin.Run()
    except KeyboardInterrupt:
        print('Ctrl-C')
    finally:
        await Plugin.StopAll()
