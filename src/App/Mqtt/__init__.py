from .Conf import *


def Main(aOwner) -> tuple:
    from .Main import TMqtt

    Obj = TMqtt()
    return (Obj, Obj.Run())
