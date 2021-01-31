import uasyncio as asyncio
from .Options import *


def Main():
    from .Main import THttpApiApp
    asyncio.create_task(THttpApiApp().Run())
