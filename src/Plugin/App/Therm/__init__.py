def Main():
    from .Main import TTherm

    Obj = TTherm()
    return (Obj, Obj.Run())
