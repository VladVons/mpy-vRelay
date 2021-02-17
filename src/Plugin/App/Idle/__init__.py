from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import TIdle

    R = TIdle()
    asyncio.create_task(R.Run())
    return R
