import uasyncio as asyncio
from .Options import *


def Main():
    from .Main import TMenuApp
    asyncio.create_task(TMenuApp().Run('m'))
