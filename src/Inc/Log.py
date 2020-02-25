'''
Author:      Vladimir Vons, Oster Inc.
Created:     2017.02.01
License:     GNU, see LICENSE for more details
Description: 
'''


import time
import os
import sys
#
from Inc.Conf import Conf


class TEcho():
    def Write(self, aMsg: str):
        pass


class TConsole(TEcho):
    def Write(self, aMsg: str):
        print(aMsg)


class TLog():
    def __init__(self):
        self.Level  = 1
        self.Cnt    = 0
        self.Echoes = [] 

        self.AddEcho(TConsole())

    def AddEcho(self, aEcho: TEcho):
        self.Echoes.append(aEcho) 

    def Print(self, aLevel: int, *aParam) -> str:
        R = '' 
        if (aLevel <= self.Level):
            self.Cnt += 1
            lt  = time.localtime(time.time())
            Now = '%d-%02d-%02d,%02d:%02d:%02d' % (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])
            R   = '%s,%03d,%d,%s,%s%s' % (Now, self.Cnt, aLevel, Conf.get('ID'), ' ' * aLevel, list(aParam))
            for Echo in self.Echoes: 
                Echo.Write(R)
        return R


Log = TLog()
