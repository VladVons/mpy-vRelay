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

        if (not UFS.FileExists(aFile +  '.py')):
            aFile = aFile + '_' + sys.platform

        self.File = aFile + '.py'
        self.Load(aFile)

    def Load(self, aFile: str):
        try:
            Obj = __import__(aFile)
            for K in dir(Obj):
                self[K] = getattr(Obj, K)
        except Exception as E: 
            Log.Print(1, 'x', 'Load()', E)

    def Save(self):
        with open(self.File, 'w') as File:
            for K, V in sorted(self.Keys().items()):
                if (type(V) is str):
                    V = "'" + V + "'"
                File.write('%s = %s\n' % (K, V))

Conf = TConf('/Options')
