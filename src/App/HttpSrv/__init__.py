from .Options import *


def Main():
    from .Main import THttpApiApp

    Obj = THttpApiApp()
    return (Obj, Obj.Run())
