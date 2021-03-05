from .Options import *


def Main():
    from Inc.Conf import Conf

    if (not Conf.STA_ESSID):
        from IncP.Captive import TCaptive

        Obj = TCaptive()
        Task = Obj.Run(Conf.get('AP_Paswd', '12345678'))
        return (Obj, Task)
