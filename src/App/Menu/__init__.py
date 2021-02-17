from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import TMenuApp
    asyncio.create_task(TMenuApp().Run('m'))
