def Main(aOwner) -> tuple:
    from .Main import THttpApiApp

    Obj = THttpApiApp()
    return (Obj, Obj.Run())
