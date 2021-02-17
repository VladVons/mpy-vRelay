from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import TWDog

    R = TWDog()
    asyncio.create_task(R.Run())
    return R
