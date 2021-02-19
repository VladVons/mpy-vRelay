from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import TTherm

    R = TTherm()
    asyncio.create_task(R.Run())
    return R
