from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import THttpApiApp

    R = THttpApiApp()
    asyncio.create_task(R.Run())
    return R
