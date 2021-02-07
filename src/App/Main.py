'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import os
import machine
import uasyncio as asyncio
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Task import Tasks
from Inc.Plugin import TPlugin
from Inc.Util import UHrd
from .Utils   import TWLanApp

#from Inc.DB.Dbl import TDbl


async def Run():
    Log.Print(1, 'i', 'Run', os.uname())

    DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    print('DSleep', DSleep)

    await UHrd.ALedFlash(Conf.get('PinLed', 2), 3, 0.5)

    Plugin = TPlugin()

    WLan = TWLanApp()
    if (Conf.STA_ESSID):
        if (await WLan.TryConnect()):
            print()

            if (not DSleep):
                from Inc.Util.UTime import SetTime
                SetTime(Conf.get('TZone', 0))

            if (Conf.Mqtt_Host):
                Plugin.LoadMod('App/Mqtt', True)
    else:
        #import App.Captive as NetCaptive
        #Captive.Main()
        Plugin.LoadMod('App/Captive', True)

    Plugin.LoadList(['App/HttpSrv', 'App/Menu'])
    Plugin.LoadDir('Plugin/App')

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('Ctrl-C')
    finally:
        Tasks.Stop()


def Main():
    asyncio.run(Run())
