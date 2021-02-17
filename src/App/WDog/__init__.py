from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import Run

    asyncio.create_task(Run())
