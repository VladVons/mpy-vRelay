#!/usr/bin/env python3

import os, sys
from Inc.Conf import TConf

def Test1(aPath):
    print('aPath:', aPath)
    __import__(aPath)
    Mod = sys.modules.get(aPath)
    Obj = getattr(Mod, 'Main')
    Obj()
    print(Obj)


File="Conf/Class/Plugin~App~Therm"
#q1 = os.stat(File + '.py')

#Test1(File)
Conf = TConf(File)
print(Conf.keys())
