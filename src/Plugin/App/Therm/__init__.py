from Inc.Conf import TConf
Conf = TConf('Conf/Therm')

#esp8266. maximum recursion depth exceeded
#from App import ConfApp
#from Inc.ConfDev import TConfDev
#ConfDev = TConfDev()
#ConfDev.Load('Conf/Dev', ConfApp)

def Main():
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run(Conf.get('Sleep', 15)))
