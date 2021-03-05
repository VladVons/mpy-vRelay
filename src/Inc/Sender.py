'''
Author:      Vladimir Vons, Oster Inc
Created:     2021.03.05
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from ucollections import deque


class TSender():
    def __init__(self, aOnSend, aLen: int = 10):
        self.Buf = deque((), aLen)
        self.OnSend = aOnSend

    async def Send(self, aData):
        if (await self.OnSend(aData)):
            # send unsend data
            for i in range(len(self.Buf)):
                await asyncio.sleep(0.5)

                Data = self.Buf.popleft()
                await self.OnSend(Data)
        else:
            self.Buf.append(aData)
