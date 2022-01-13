'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.01.30
License:     GNU, see LICENSE for more details
Description:
'''


try:
  import asyncio
except:
  import uasyncio as asyncio

import os, sys, gc
#
from Inc.Log  import Log


class TPlugin(dict):
    def AddTask(self, aModule, aPath):
        gc.collect()
        Log.Print(1, 'i', 'MemFree %6d. Loading %s ...' % (gc.mem_free(), aPath))
        Arr = aModule.Main(self)
        if (Arr):
            #Class, Func, ?Topic = Arr
            self[aPath] = [Arr[0], asyncio.create_task(Arr[1])]

    def LoadDir(self, aDir: str):
        Files = os.ilistdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir.replace('/', '.') + '.' + DirName)

    def LoadList(self, aModules: str):
        for Module in aModules.split(' '):
            self.LoadMod(Module)

    def LoadMod(self, aPath: str):
        if (aPath == '') or (aPath.startswith('-')) or (self.get(aPath)):
            return

        __import__(aPath)
        Mod = sys.modules.get(aPath)
        Depends = getattr(Mod, 'Depends', '')
        for Item in Depends.split(' '):
            self.LoadMod(Item)

        self.AddTask(Mod, aPath)

    async def _Post(self, aTasks, aOwner, aMsg, aFunc) -> dict:
        R = {}
        for Key, (Class, Task) in aTasks:
            if (Class != aOwner) and (hasattr(Class, aFunc)):
                Func = getattr(Class, aFunc)
                R[Key] = await Func(aOwner, aMsg)
                if (R[Key] == aOwner):
                    break
        return R

    async def Post(self, aOwner, aMsg, aFunc: str = '_DoPost'):
        return await self._Post(self.items(), aOwner, aMsg, aFunc)

    def PostNonAsync(self, aOwner, aMsg, aFunc: str = '_DoPost'):
        return asyncio.run(self.Post(aOwner, aMsg, aFunc))

    async def Stop(self, aPath: str) -> bool:
        Obj = self.get(aPath)
        if (Obj):
            await self._Post([(aPath, Obj)], None, None, '_DoStop')
            await asyncio.sleep(1)
            Obj[1].cancel()
            del self[aPath]
            return True

    async def StopAll(self):
        for Key in self.keys():
            await self.Stop(Key)

    async def Run(self):
        Tasks = [v[1] for v in self.values()]
        await asyncio.gather(*Tasks)


Plugin = TPlugin()
