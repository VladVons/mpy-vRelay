'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio


class TTask():
    Sleep  = 1
    Cnt    = 0

    async def Loop(self):
        self.Handle = self.Run = True
        try:
            while self.Run:
                if (self.Handle):
                    self.Cnt += 1
                    self.DoLoop()
                await asyncio.sleep(self.Sleep)
        finally:
            self.DoExit()

    def DoLoop(self):
        pass

    def DoExit(self):
        pass


class TTasks():
    def __init__(self):
        self.Obj = []
        self.ELoop = asyncio.get_event_loop()

    def Add(self, aTask: TTask):
        if (aTask not in self.Obj):
            self.Obj.append(aTask)
            self.ELoop.create_task(aTask.Loop())

    def Stop(self):
        for O in self.Obj:
            O.Run = False
            O.DoExit()

    def Run(self):
        self.ELoop.run_forever()


Tasks = TTasks()
