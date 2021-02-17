'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.01.30
License:     GNU, see LICENSE for more details
Description:
'''

import os, sys, gc
#
from Inc.Log  import Log
from Inc.Util.UFS import FileLoad


class TPlugin():
    def __init__(self):
        self.Data = {}
 
    def LoadDir(self, aDir: str):
        Files = os.ilistdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir + '/' + DirName, False)

    def LoadList(self, aModules: list):
        for Module in aModules:
            self.LoadMod(Module)

    def LoadMod(self, aPath: str, aForce: bool = True):
        if (not self.Data.get(aPath)):
            gc.collect()
            MemStart = gc.mem_free()

            Mod = __import__(aPath)
            if (aForce) or (getattr(Mod, 'AutoLoad', False)):
                self.Data[aPath] = Mod
                Mod.Main()

                gc.collect()
                Log.Print(1, 'i', 'Load()', 'Path %s, MemHeap %d, MemFree %d' % (aPath, MemStart - gc.mem_free(), gc.mem_free()))
            else:
                del Mod
                for Item in sys.modules:
                    if (aPath in Item):
                        del sys.modules[Item]
