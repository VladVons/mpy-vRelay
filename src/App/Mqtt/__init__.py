from .Conf import *


def Main() -> tuple:
    from .Main import TMqtt

    Obj = TMqtt()
    return (Obj, Obj.Run())
