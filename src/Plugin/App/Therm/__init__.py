from Inc.Conf import TConf

ConfTherm = TConf('ConfTherm')

def Main():
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run())
