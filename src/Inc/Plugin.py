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


class TPlugin():
    def __init__(self):
        self.Data = {}

    @staticmethod
    def Run():
        Loop = asyncio.get_event_loop()
        Loop.run_forever()

    def LoadDir(self, aDir: str):
        Files = os.ilistdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir + '.' + DirName)

    def LoadList(self, aModules: str):
        for Module in aModules.split(' '):
            self.LoadMod(Module)

    def LoadMod(self, aPath: str):
        if (aPath == '') or (aPath.startswith('-')) or (self.Data.get(aPath)):
            return

        __import__(aPath)
        Mod = sys.modules.get(aPath)
        Depends = getattr(Mod, 'Depends', '')
        for Item in Depends.split(' '):
            self.LoadMod(Item)

        Arr = Mod.Main()
        if (Arr):
            # Class, Func = Arr
            self.Data[aPath] = Arr[0]
            asyncio.create_task(Arr[1])

            Log.Print(1, 'i', 'LoadMod()', 'Path %s' % (aPath))
        gc.collect()

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


Plugin = TPlugin()
