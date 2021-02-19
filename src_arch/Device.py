#!/usr/bin/micropython


class TDev():
    pass


class TDevDHT22(TDev):
    def __init__(self, aPin):
        #self.Obj = DHT22(aPin)
        self.Value = []

    async def Read(self):
        Value = await self.Obj.Get()


class TUnit():
    def __init__(self):
        self.Dev = {}

    def Read(self):
        for Dev in self.Dev.values():
            Dev.Get()


#DevDHT22 = TDevDHT22(14)
#print(dir(DevDHT22), DevDHT22.__class__)
#print(DevDHT22.__class__.__name__)

import random
#print(random.randint(1, 10))
print(dir(random))

