from .Options import *


def Main():
    from Inc.Captive import TCaptive

    Obj = TCaptive()
    return (Obj, Obj.Run('192.168.4.1'))
