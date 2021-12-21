from Inc.Conf import TConf

ConfTherm = TConf('Conf/Therm')

def Main():
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run())
