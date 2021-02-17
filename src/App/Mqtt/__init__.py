from .Options import *


def Main():
    import uasyncio as asyncio
    from Inc.Conf import Conf
    from .Main import TMqtt

    R = TMqtt()
    asyncio.create_task(R.Run(Conf.Mqtt_Host, Conf.get('Mqtt_Port', 1883), Conf.Mqtt_User, Conf.Mqtt_Passw))
    return R
