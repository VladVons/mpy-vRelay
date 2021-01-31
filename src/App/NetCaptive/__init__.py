from .Options import *


async def GetIP():
    from App.Utils import TWLanApp

    WLan = TWLanApp()
    APIF = await WLan.EnableAP(True)
    IP = APIF.ifconfig()[0]
    return IP

def Main():
    import uasyncio as asyncio
    from Inc.Task import Tasks
    from .Main import TTaskCaptive

    IP = asyncio.run(GetIP())
    Tasks.Add(TTaskCaptive(IP), 0.1)
