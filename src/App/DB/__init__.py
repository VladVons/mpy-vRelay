def Main(aConf):
    from .Main import TDB

    Obj = TDB()
    return (Obj, Obj.Run('values.db'))
