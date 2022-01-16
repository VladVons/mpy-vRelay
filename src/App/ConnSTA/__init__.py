def Main(aConf) -> tuple:
    from .Main import TConnSTA

    Obj = TConnSTA()
    return (Obj, Obj.Run(60))
