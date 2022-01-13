def Main(aOwner):
    from .Main import TIdle

    Obj = TIdle()
    return (Obj, Obj.Run())
          