from .Options import *


def Main():
    from .Main import TDoorCheck

    Obj = TDoorCheck(cPinBtn, cPinLed, cPinSnd)
    return (Obj, Obj.Run())
