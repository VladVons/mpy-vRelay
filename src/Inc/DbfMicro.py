'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.29
License:     GNU, see LICENSE for more details
Description:.
'''

import os
import struct
import collections


CHead  = collections.namedtuple('Head',  ['Sign', 'RecCnt', 'LUpd', 'HeadLen', 'RecLen'])
CField = collections.namedtuple('Field', ['Name', 'Type', 'Len', 'LenD'])


class TDbf():
    def __init__(self):
        self.Stream  = None
        self.Head    = None
        self.Fields  = None
        self.RecNo   = 0
        self.RecSave = False

    def __del__(self):
        self.Close()

    def _GetFieldRange(self, aIdx: int):
        R = 0
        for F in self.Fields[0:aIdx + 1]:
            print(F.Name, F.Len)
            R += F.Len
        return [R, F.Len]

    def _ParseFields(self):
        self.Fields = []

        self.Stream.seek(32)
        while True:
            Data = self.Stream.read(32)
            FName, FType, X, FLen, FLenD = struct.unpack('11s1s4s1B1B', Data[0:11+1+4+1+1])
            if (FName[0] == 13):
                break

            F = CField(
                    Name = FName.split(b'\0',1)[0].decode(), 
                    Type = FType.decode(), 
                    Len  = FLen, 
                    LenD = FLenD
                )
            self.Fields.append(F)

    def _ParseHead(self):
        self.Stream.seek(0)
        Data = self.Stream.read(32)
        Sign, LUpd, RecCnt, HeadLen, RecLen = struct.unpack('1B3s1I1H1H', Data[0:1+3+4+2+2])
        self.Head = CHead(
                Sign    = Sign,
                LUpd    = LUpd,
                RecCnt  = RecCnt,
                HeadLen = HeadLen, 
                RecLen  = RecLen 
            )

    def _SeekRecNo(self):
        self.Stream.seek(self.Head.HeadLen + (self.RecNo * self.Head.RecLen))

    def Open(self, aName: str) -> bool:
        self.Name   = aName
        self.Stream = open(aName, 'rb')
 
        self._ParseHead()
        self._ParseFields()
        self.RecGo(0)

    def Close(self): 
       if (self.Stream):
            self.RecWrite()
            self.Stream.close()

    def GetSize(self) -> int:
        Len = os.stat(self.Name)[6]
        return int((Len - self.Head.HeadLen) / self.Head.RecLen)

    def RecRead(self):
        self._SeekRecNo()
        self.Buf = self.Stream.read(self.Head.RecLen)

    def RecWrite(self):
        if (self.RecSave):
            self._SeekRecNo()
            self.Stream.write(self.Buf)
            self.RecSave = False

    def RecGo(self, aNo: int):
        self.RecWrite()
        self.RecNo = min(max(0, aNo), self.GetSize())
        self.RecRead()

    def GetFieldData(self, aIdx: int):
        Arr = self._GetFieldRange(aIdx)
        print(Arr)
        return self.Buf[Arr[0]:Arr[1]]
