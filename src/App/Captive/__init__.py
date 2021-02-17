from .Options import *


def Main():
    import uasyncio as asyncio
    from Inc.Captive import TCaptive

    asyncio.create_task(TCaptive().Run('192.168.4.1'))
