def Main(aConf) -> tuple:
    from .Main import TSim7000

    Obj = TSim7000()
    return (Obj, Obj.Run())
