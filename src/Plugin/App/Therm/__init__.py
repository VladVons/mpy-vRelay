def Main(aConf):
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run(aConf.get('Sleep', 5)))
