from .Options import *


def Main():
    from Inc.Conf import Conf
    from Inc.Task import Tasks
    from .Main import TTaskIdle

    Tasks.Add(TTaskIdle(), Conf.get('TIdle', 1), 'idle')
