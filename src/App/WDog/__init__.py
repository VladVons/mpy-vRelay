def Main(aConf) -> tuple:
    from .Main import TWDog

    Obj = TWDog()
    return (Obj, Obj.Run())
