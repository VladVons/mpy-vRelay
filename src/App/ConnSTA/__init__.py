from .Options import *


def Main():
    from .Main import TConnSTA

    Obj = TConnSTA()
    return (Obj, Obj.Run(5))
