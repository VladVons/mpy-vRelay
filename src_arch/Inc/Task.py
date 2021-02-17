'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import sys
import uasyncio as asyncio
#
from .Log import Log


class TTask():
    # Alias 
    # Parent
    # Task
    # Pause
    # IsRun
    Cnt: int    = 0
    Sleep: int  = 1

    async def Run(self):
        await self.DoEnter()

        self.Pause = False
        self.IsRun = True
        while self.IsRun:
            if (not self.Pause):
                self.Cnt += 1
                await self.DoLoop()
            await asyncio.sleep(self.Sleep)
        await self.DoExit()

    async def DoEnter(self):
        pass

    async def DoLoop(self):
        pass

    async def DoExit(self):
        pass

    async def DoPost(self, aOwner: TTask, aMsg):
        pass


class TTasks():
    def __init__(self):
        self.Obj = []

    def Add(self, aTask: TTask, aSleep: int = 1, aAlias: str = ''):
        if (aTask not in self.Obj):
            if (not aAlias):
                aAlias = type(aTask).__name__

            aTask.Alias = aAlias
            aTask.Task  = aTask.Run()
            aTask.Sleep = aSleep
            aTask.Parent = self
            self.Obj.append(aTask)
            ELoop.create_task(aTask.Task)

    def Find(self, aAlias: str) -> TTask:
        for O in self.Obj:
            if (O.Alias == aAlias):
                return O

    async def Remove(self, aTask):
        await aTask.DoExit()
        aTask.Task.cancel()
        self.Obj.remove(aTask)

    async def Stop(self):
        for Obj in self.Obj:
            await Obj.DoExit()
            Obj.IsRun = False

    async def Post(self, aOwner: TTask, aMsg):
        for Obj in self.Obj:
            if (Obj != aOwner):
                if (await Obj.DoPost(aOwner, aMsg)):
                    break

    def Run(self):
        ELoop.run_forever()


ELoop = asyncio.get_event_loop()
Tasks = TTasks()
