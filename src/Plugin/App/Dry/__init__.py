#Enable = False

def Main(aConf):
    from .Main import TDry

    Obj = TDry()
    return (Obj, Obj.Run(aConf.get('Sleep', 1)))
