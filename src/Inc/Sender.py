'''
Author:      Vladimir Vons, Oster Inc
Created:     2021.03.05
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from ucollections import deque


class TSender():
    def __init__(self, aSender, aLen: int = 10):
        self.Buf = deque((), aLen)
        self.Sender = aSender

    async def Send(self, aData):
        if (await self.Sender(aData)):
            # send unsend data
            for i in range(len(self.Buf)):
                await asyncio.sleep(0.5)

                Data = self.Buf.popleft()
                await self.Sender(Data)
        else:
            self.Buf.append(aData)
