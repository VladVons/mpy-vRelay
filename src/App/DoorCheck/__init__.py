from .Conf import *


def Main(aConf) -> tuple:
    from .Main import TDoorCheck

    Obj = TDoorCheck(cPinBtn, cPinLed, cPinSnd)
    return (Obj, Obj.Run())
