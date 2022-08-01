#Enable = False

def Main(aConf):
    from .Main import TIdle

    Obj = TIdle()
    return (Obj, Obj.Run())
