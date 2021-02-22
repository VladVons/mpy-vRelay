'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.01.30
License:     GNU, see LICENSE for more details
Description:
'''

import os, sys, gc
import uasyncio as asyncio
#
from Inc.Log  import Log


class TPlugin():
    def __init__(self):
        self.Data = {}

    @staticmethod
    def DelMod(aPath, aMod):
        del aMod
        for Item in sys.modules:
            if (aPath in Item):
                del sys.modules[Item]

    def LoadDir(self, aDir: str):
        Files = os.ilistdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir + '/' + DirName, False)

    def LoadList(self, aModules: str):
        for Module in aModules.split(' '):
            self.LoadMod(Module)

    def LoadMod(self, aPath: str, aForce: bool = True):
        if (aPath == '') or (aPath.startswith('-')) or (self.Data.get(aPath)):
            return

        gc.collect()
        MemStart = gc.mem_free()

        Mod = __import__(aPath)
        if (aForce) or (getattr(Mod, 'AutoLoad', False)):
            Depends = getattr(Mod, 'Depends', '')
            for Item in Depends.split(' '):
                self.LoadMod(Item, True)

            Arr = Mod.Main()
            if (Arr):
                # Class, Func = Arr
                self.Data[aPath] = Arr[0]
                asyncio.create_task(Arr[1])

                gc.collect()
                Log.Print(1, 'i', 'LoadMod()', 'Path %s, MemHeap %d, MemFree %d' % (aPath, MemStart - gc.mem_free(), gc.mem_free()))

                return Mod
            else:
                self.DelMod(aPath, Mod)
        else:
            self.DelMod(aPath, Mod)

    def Get(self, aPath: str):
        return self.Data.get(aPath)

    async def Post(self, aOwner, aMsg, aFunc = '_DoPost'):
        R = {}
        for Key, Obj in self.Data.items():
            if (Obj != aOwner) and (hasattr(Obj, aFunc)):
                Func = getattr(Obj, aFunc)
                R[Key] = await Func(aOwner, aMsg)
        return R

    async def Stop(self):
        return await self.Post(None, 'Stop')

    @staticmethod
    def Run():
        Loop = asyncio.get_event_loop()
        Loop.run_forever()



Plugin = TPlugin()
