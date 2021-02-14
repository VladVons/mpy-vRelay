import uasyncio as asyncio
from .Options import *


def Main():
    from .Main import Run
    asyncio.create_task(Run())
