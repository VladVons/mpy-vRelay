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
from .Utils   import TWLanApp
#from Inc.DB.Dbl import TDbl


async def Run():
    Log.Print(1, 'i', 'Run', os.uname())

    DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    print('DSleep', DSleep)

    from App.Menu import TMenuApp
    asyncio.create_task(TMenuApp().Run('m'))

    WLan = TWLanApp()
    if (Conf.STA_ESSID):
        if (await WLan.TryConnect()):
            print()

            if (not DSleep):
                from Inc.Util.UTime import SetTime
                SetTime(Conf.get('TZone', 0))

            if (Conf.Mqtt_Host):
                from Inc.NetMqtt import TTaskMqtt
                Tasks.Add(TTaskMqtt(Conf.Mqtt_Host, Conf.get('Mqtt_Port', 1883), Conf.Mqtt_User, Conf.Mqtt_Passw), 0.1, 'mqtt')
    else:
        Log.Print(1, 'i', 'NetCaptive')
        APIF = await WLan.EnableAP(True)
        IP = APIF.ifconfig()[0]

        from Inc.NetCaptive import TTaskCaptive
        Tasks.Add(TTaskCaptive(IP), 0.1)

    from App.Http import THttpApiApp
    asyncio.create_task(THttpApiApp().Run())

    from App.Idle import TTaskIdle
    Tasks.Add(TTaskIdle(), Conf.get('TIdle', 2), 'idle')

    #from App.DoorCheck import TTaskDoorCheck
    #Tasks.Add(TTaskDoorCheck(Conf.get('PinBtn', 0), Conf.get('PinLed', 2), Conf.get('PinSnd', 13)), 0.5, 'door')

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('Ctrl-C')
    finally:
        Tasks.Stop()


def Main():
    asyncio.run(Run())
