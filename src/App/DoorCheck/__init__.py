from .Conf import *


def Main(aOwner):
    from .Main import TDoorCheck

    Obj = TDoorCheck(cPinBtn, cPinLed, cPinSnd)
    return (Obj, Obj.Run())
