def Main(aConf) -> tuple:
    from .Main import THttpApiApp

    Obj = THttpApiApp()
    return (Obj, Obj.Run())
