'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import sys
import uasyncio as asyncio
from .Log import Log


Tasks = None


class TTask():
    Alias  = ''
    Cnt    = 0
    Sleep  = 1

    async def Loop(self):
        self.Pause = False
        self.Run   = True
        while self.Run:
            try:
                self.DoEnter()
                while self.Run:
                    if (not self.Pause):
                        self.Cnt += 1
                        self.DoLoop()
                    await asyncio.sleep(self.Sleep)
            except Exception as E:
                Sleep = self.DoExcept(E)
                if (Sleep == 0):
                    Tasks.Remove(self)
                    break
                await asyncio.sleep(Sleep)
        self.DoExit()

    def DoEnter(self):
        pass

    def DoLoop(self):
        pass

    def DoExit(self):
        pass

    def DoExcept(self, aE):
        sys.print_exception(aE)
        Log.Print(1, 'Exit', self.__class__.__name__, self.Alias)
        return 0


class TTasks():
    def __init__(self):
        self.Obj = []
        self.ELoop = asyncio.get_event_loop()

    def Add(self, aTask: TTask, aSleep: int = 1, aAlias: str = ''):
        if (aTask not in self.Obj):
            aTask.Alias = aAlias
            aTask.Sleep = aSleep
            self.Obj.append(aTask)
            self.ELoop.create_task(aTask.Loop())

    def Find(self, aAlias: str) -> TTask:
        for O in self.Obj:
            if (O.Alias == aAlias):
                return O
        return None

    def Remove(self, aTask):
        self.Obj.remove(aTask)

    def Stop(self):
        for O in self.Obj:
            O.DoExit()
            O.Run = False

    def Run(self):
        self.ELoop.run_forever()


Tasks = TTasks()
