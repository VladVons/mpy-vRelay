def Main(aConf) -> tuple:
    from .Main import TMenuApp

    Obj = TMenuApp()
    return (Obj, Obj.Run('m'))
