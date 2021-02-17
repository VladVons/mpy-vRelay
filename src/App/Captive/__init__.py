from .Options import *


def Main():
    import uasyncio as asyncio
    from Inc.Captive import TCaptive

    R = TCaptive()
    asyncio.create_task(R.Run('192.168.4.1'))
    return R
