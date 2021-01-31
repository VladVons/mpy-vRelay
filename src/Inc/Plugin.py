'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.01.30
License:     GNU, see LICENSE for more details
Description:
'''

import os
#
from Inc.Log  import Log


class TPlugin():
    def __init__(self):
        self.Data = {}
 
    def LoadDir(self, aDir: str):
        Files = os.ilistdir(aDir)
        for Info in Files:
            if (Info[1] & 0x4000): # is dir
                DirName = Info[0]
                self.LoadMod(aDir + '/' + DirName)

    def LoadList(self, aModules: list):
        for Module in aModules:
            self.LoadMod(Module)

    def LoadMod(self, aPath: str, aForce: bool = False):
        if (not self.Data.get(aPath)):
            Mod = __import__(aPath)
            if (aForce or getattr(Mod, 'AutoLoad', False)):
                Log.Print(1, 'i', 'Load()', aPath)
                self.Data[aPath] = Mod
                Mod.Main()
