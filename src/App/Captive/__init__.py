from .Options import *


def Main() -> tuple:
    from App import ConfApp

    if (not ConfApp.STA_ESSID):
        from IncP.Captive import TCaptive

        Obj = TCaptive()
        Task = Obj.Run(ConfApp.get('AP_Paswd', '12345678'))
        return (Obj, Task)
