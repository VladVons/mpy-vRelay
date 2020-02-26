'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
from Inc.Log import Log


class TTask():
    Sleep  = 1
    Cnt    = 0
    Alias  = ''

    async def Loop(self):
        self.Handle = self.Run = True
        while self.Run:
            try:
                self.DoEnter()
                while self.Run:
                    if (self.Handle):
                        self.Cnt += 1
                        self.DoLoop()
                    await asyncio.sleep(self.Sleep)
            except Exception as E:
                Sleep = self.DoExcept(E)
                if (Sleep == 0):
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
        Log.Print(1, 'Err', self.__class__.__name__, aE)
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

    def Stop(self):
        for O in self.Obj:
            O.DoExit()
            O.Run = False

    def Run(self):
        self.ELoop.run_forever()


Tasks = TTasks()
