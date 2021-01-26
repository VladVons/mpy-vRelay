'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import sys

try:
    import uasyncio as asyncio
except:
    from .Pip import Install
    #Install('uasyncio')

from .Log import Log


Tasks = None


class TTask():
    # Alias 
    # Parent
    # Pause
    # IsRun
    Cnt: int    = 0
    Sleep: int  = 1

    async def Run(self):
        self.Pause = False
        self.IsRun = True
        while self.IsRun:
            try:
                self.DoEnter()
                while self.IsRun:
                    if (not self.Pause):
                        self.Cnt += 1
                        await self.DoLoop()
                    await asyncio.sleep(self.Sleep)
            except Exception as E:
                sys.print_exception(E)
                Sleep = self.DoExcept(E)
                if (not Sleep):
                    Sleep = 0
                    Tasks.Remove(self)
                    break
                await asyncio.sleep(Sleep)
        self.DoExit()

    def DoEnter(self):
        pass

    async def DoLoop(self):
        pass

    def DoExit(self):
        pass

    def DoExcept(self, aE):
        pass

    async def DoPost(self, aOwner: TTask, aMsg):
        pass


class TTasks():
    def __init__(self):
        self.Obj = []
        self.ELoop = asyncio.get_event_loop()

    def Add(self, aTask: TTask, aSleep: int = 1, aAlias: str = ''):
        if (aTask not in self.Obj):
            if (not aAlias):
                aAlias = type(aTask).__name__
            aTask.Alias = aAlias
 
            aTask.Sleep  = aSleep
            aTask.Parent = self
            self.Obj.append(aTask)
            self.ELoop.create_task(aTask.Run())

    def Find(self, aAlias: str) -> TTask:
        for O in self.Obj:
            if (O.Alias == aAlias):
                return O
        return None

    def Remove(self, aTask):
        self.Obj.remove(aTask)

    def Stop(self):
        for Obj in self.Obj:
            Obj.DoExit()
            Obj.IsRun = False

    def Post(self, aOwner: TTask, aMsg):
        for Obj in self.Obj:
            if (Obj != aOwner):
                if (await Obj.DoPost(aOwner, aMsg)):
                    break

    def Run(self):
        self.ELoop.run_forever()


Tasks = TTasks()
