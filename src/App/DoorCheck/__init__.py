from .Options import *


def Main():
    import uasyncio as asyncio
    from Inc.Conf import Conf
    from .Main import TDoorCheck

    R = TDoorCheck(cPinBtn, cPinLed, cPinSnd)
    asyncio.create_task(R.Run())
    return R
