async def Task1():
    import uasyncio as asyncio

    Cnt = 0
    while True:
        Cnt += 1
        print('Task1', Cnt)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        await asyncio.sleep(3)
 
def Test1():
    import uasyncio as asyncio
    from Inc import UHrd

    WDog = UHrd.TWDog(0, 10)

    Loop = asyncio.get_event_loop()
    Loop.create_task(Task1())
    Loop.run_forever()


def Connect(aESSID: str, aPassw: str, aCnt: int = 20) -> bool:
    import sys
    import network

    Obj = network.WLAN(network.STA_IF)
    R = Obj.isconnected()
    if (not R):
        Obj.active(True)
        Obj.connect(aESSID, aPassw)

        while (not Obj.isconnected()) and (aCnt > 0):
            sys.stdout.write('.')
            time.sleep(1)
            aCnt -= 1
        R = aCnt > 0

    print('Network', Obj.ifconfig())
    return R


def TestMem():
    print('')

    import gc
    print('mem_free', gc.collect(), gc.mem_free())

    import uasyncio
    print('mem_free', gc.collect(), gc.mem_free())

    import umqtt.simple
    print('mem_free', gc.collect(), gc.mem_free())


#Test1()
