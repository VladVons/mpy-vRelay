import uasyncio as asyncio
from machine import WDT


async def Run():
    #ESP32
    #wdt = WDT(timeout = Conf.get('WatchDog', 30 * 1000))

    # ESP8266 has no param and def value 2500 msec
    #wdt = WDT()
    print('---x1')
    while True:
        print('---x2')
        #wdt.feed()
        await asyncio.sleep(0.5)
        print('---x3')
