from .Options import *


def Main():
    from .Main import TSim7000

    Obj = TSim7000()
    return (Obj, Obj.Run())
