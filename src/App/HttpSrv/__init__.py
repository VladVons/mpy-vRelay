def Main() -> tuple:
    from .Main import THttpApiApp

    Obj = THttpApiApp()
    return (Obj, Obj.Run())
