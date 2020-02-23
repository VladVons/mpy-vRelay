'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio


class TTask():
    Sleep = 1

    async def Run(self):
        self.Handle = self.IsRun = True
        while self.IsRun:
            if (self.Handle):
                self.DoRun()
            await asyncio.sleep(self.Sleep)
        self.DoExit()

    def DoRun(self):
        pass

    def DoExit(self):
        pass
