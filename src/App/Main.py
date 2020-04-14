'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import os
import machine
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Task import Tasks
from .Utils   import TWLanApp
#from Inc.DB.Dbl import TDbl


def Run():
    Log.Print(1, 'i', 'Main', os.uname())

    DSleep = (machine.reset_cause() == machine.DEEPSLEEP_RESET)
    print('DSleep', DSleep)

    if (Conf.STA_ESSID):
        WLan = TWLanApp()
        if (WLan.TryConnect()):
            print()

            if (not DSleep):
                from Inc.Util.UTime import SetTime
                SetTime(Conf.get('TZone', 0))

            #if (Conf.Mqtt_Host):
            #    from Inc.NetMqtt import TTaskMqtt
            #    Tasks.Add(TTaskMqtt(Conf.Mqtt_Host), 0.1, 'mqtt')
    else:
        from Inc.NetCaptive import TTaskCaptive
        Tasks.Add(TTaskCaptive(), 0.1)

    from App.Idle import TTaskIdle
    Tasks.Add(TTaskIdle(), Conf.get('TIdle', 2), 'idle')

    from App.Http import THttpApiApp
    from Inc.NetHttp import TTaskHttpServer
    Tasks.Add(TTaskHttpServer(THttpApiApp()), aAlias = 'http')

    #from App.DoorCheck import TTaskDoorCheck
    #Tasks.Add(TTaskDoorCheck(Conf.get('PinBtn', 0), Conf.get('PinLed', 2), Conf.get('PinSnd', 13)), 0.5, 'door')

    try:
        Tasks.Run()
    except KeyboardInterrupt:
        print('CTRL-C')
    finally:
        Tasks.Stop()
