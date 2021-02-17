from .Options import *


def Main():
    from .Main import TIdle

    asyncio.create_task(TIdle().Run())
