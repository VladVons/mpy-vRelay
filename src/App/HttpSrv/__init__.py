from .Options import *


def Main():
    import uasyncio as asyncio
    from .Main import THttpApiApp

    asyncio.create_task(THttpApiApp().Run())
