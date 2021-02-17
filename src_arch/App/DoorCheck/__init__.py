from .Options import *


def Main():
    from Inc.Conf import Conf
    from Inc.Task import Tasks
    from .Main import TTaskDoorCheck

    Tasks.Add(TTaskDoorCheck(Conf.get('PinBtn', 0), Conf.get('PinLed', 2), Conf.get('PinSnd', 13)), 0.5, 'door')
