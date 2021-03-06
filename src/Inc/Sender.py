'''
Author:      Vladimir Vons, Oster Inc
Created:     2021.03.05
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from ucollections import deque


class TSender():
    def __init__(self, aOnSend, aSize: int = 10):
        self.Buf = deque((), aSize)
        self.OnSend = aOnSend

    async def Send(self, aData):
        if (await self.OnSend(aData)):
            # send unsend data
            for i in range(len(self.Buf)):
                await asyncio.sleep(0.5)

                Data = self.Buf.popleft()
                if (not await self.OnSend(Data)):
                    break
        else:
            self.Buf.append(aData)
