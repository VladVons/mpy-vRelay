import uasyncio as asyncio
from Inc import UHrd


async def Task1():
    Cnt = 0
    while True:
        Cnt += 1
        print('Task1', Cnt)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        await asyncio.sleep(3)
 
def Test1():
    WDog = UHrd.TWDog(0, 10)

    Loop = asyncio.get_event_loop()
    Loop.create_task(Task1())
    Loop.run_forever()

Test1()


