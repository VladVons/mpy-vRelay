from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import TMenuApp

    R = TMenuApp()
    asyncio.create_task(R.Run('m'))
    return R
