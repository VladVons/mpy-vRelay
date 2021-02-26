from .Options import *


def Main():
    from Inc.Conf import Conf

    if (not Conf.STA_ESSID):
        from IncP.Captive import TCaptive

        Obj = TCaptive()
        return (Obj, Obj.Run())
