from App import ConfApp

from Inc.Conf import TConf
ConfTherm = TConf('Conf/Therm')

#esp8266. maximum recursion depth exceeded
#from Inc.ConfDev import TConfDev
#ConfDevTherm = TConfDev()
#ConfDevTherm.Load('Conf/Dev', ConfApp)
from App import ConfDevTherm


def Main():
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run())
