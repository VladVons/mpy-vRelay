from .Options import *


def Main():
    from Inc.Conf import Conf
    from Inc.Task import Tasks
    from Inc.NetMqtt import TTaskMqtt
    Tasks.Add(TTaskMqtt(Conf.Mqtt_Host, Conf.get('Mqtt_Port', 1883), Conf.Mqtt_User, Conf.Mqtt_Passw), 0.1, 'mqtt')
