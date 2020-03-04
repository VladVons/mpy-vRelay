'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:.
'''

import os


class TDb():
    def __init__(self):
        self.Stream  = None
        self.HeadLen = 0
        self.RecLen  = 0
        self.RecNo   = 0
        self.RecSave = False
        self.Buf     = bytearray()    
        self.RecFill = b'\0'

    def __del__(self):
        self.Close()

    def __iter__(self):
        return self

    def __next__(self):
        if (self.RecNo >= self.GetSize()):
            raise StopIteration
        else:
            self.RecGo(self.RecNo)
            self.RecNo += 1
            return self.RecNo - 1

    def _SeekRecNo(self):
        Ofst = self.HeadLen + (self.RecNo * self.RecLen)
        return self.Stream.seek(Ofst)

    def Close(self): 
       if (self.Stream):
            self.RecWrite()
            self.Stream.close()
            self.Stream = None

    def GetSize(self) -> int:
        FileSize = self.Stream.seek(0, 2)
        return int((FileSize - self.HeadLen) / self.RecLen)

    def RecRead(self):
        self._SeekRecNo()
        self.Buf = bytearray(self.Stream.read(self.RecLen))

    def RecWrite(self):
        if (self.RecSave):
            self.RecSave = False
            self._SeekRecNo()
            return self.Stream.write(self.Buf)

    def RecGo(self, aNo: int):
        self.RecWrite()
        if (aNo > 0):
            self.RecNo = min(aNo, self.GetSize())
        else:
            self.RecNo = max(0, self.GetSize() + aNo)
        self.RecRead()

    def RecAdd(self):
        self.RecWrite()

        self.Buf = bytearray(self.RecFill * self.RecLen)
        self.Stream.seek(0, 2)
        self.Stream.write(self.Buf)
        self.RecNo = self.GetSize()

    def Open(self, aName: str, aReadOnly = False):
        self.Close()

        Mode = 'rb' if aReadOnly else 'rb+'
        self.Stream = open(aName, Mode)
        self._StructRead()

        self.RecGo(0)
