from Inc.Conf import TConf
Conf = TConf('Conf/Plugin.App.Therm')

#esp8266. maximum recursion depth exceeded
#from App import ConfApp
#from Inc.ConfClass import TConfClass
#ConfClass = TConfClass()
#ConfClass.Load('Conf/Class', ConfApp)

def Main(aOwner):
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run(Conf.get('Sleep', 15)))
