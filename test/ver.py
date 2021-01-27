#!/usr/bin/env python3

import os
import json

def GetData(aDir):
    Ver   = '1.0.11'
    Size  = 0
    Names = []

    for Root, Subdirs, Files in os.walk(aDir):
        Files.sort()
        for File in Files:
            if (File.startswith('ver.') or File.startswith('.')):
                #print('Skip', File)
                continue

            Name = ('%s%s' if Root.endswith('/') else '%s/%s') % (Root, File)
            Names.append(Name.replace(aDir, ''))

            Len = int(os.stat(Name)[6])
            Size += Len
            print(Len, Name)

    Res = {"Ver": Ver, "Size": Size, "Files": Names}
    return Res


def Export(aFile, aDir = './'):
    Data = GetData(aDir)
    with open(aFile, 'w') as hFile:
        json.dump(Data, hFile)

#Export('ver.json', '../src')
Export('ver.json')
