def Main(aConf) -> tuple:
    from .Main import TDB

    Obj = TDB('values.db')
    return (Obj, Obj.Run(60))
