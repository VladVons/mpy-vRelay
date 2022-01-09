'''
Author:      Vladimir Vons, Oster Inc.
Created:     2018.06.10
License:     GNU, see LICENSE for more details
Description:.

abrevation for RAM saving
R - Result
K - Key
V - Value
'''


import os, sys
#
from .Util import UFS
from .Log  import Log


class TConfD(dict):
    def __getattr__(self, aName: str):
        return self.get(aName)

    def Keys(self) -> dict:
        R = {}
        for K in self.keys(): 
            if ('__' not in K):
                R[K] = self.get(K)
        return R


class TConf(TConfD):
    def __init__(self, aFile: str):
        super().__init__() 
        self.LoadPlatform(aFile)

    def LoadPlatform(self, aFile: str):
        self.File = aFile + '.py'
        for File in [aFile, aFile + '_' + sys.platform]:
            if (UFS.FileExists(File +  '.py')):
                self.Load(File)

    def Load(self, aFile: str):
        Obj = __import__(aFile)
        #Obj = __import__(aFile.replace('/', '.'), None, None, ['App'])
        for Key in dir(Obj):
            if (not Key.startswith('__')):
                self[Key] = getattr(Obj, Key, None)

    def Save(self):
        with open(self.File, 'w') as File:
            for K, V in sorted(self.Keys().items()):
                if (type(V) is str):
                    V = "'" + V + "'"
                File.write('%s = %s\n' % (K, V))

#Conf = TConf('ConfApp')
