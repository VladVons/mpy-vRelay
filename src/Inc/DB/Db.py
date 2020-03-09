'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:.
'''

from Inc.Util import UArr

# ToDo. < 3.7 doesnt supports defaults parameter. Need own TField
#CField = collections.namedtuple('Field', ('Type', 'Len', 'LenD', 'No', 'Ofst'), defaults = ('C', 10, 0, 0, 0))
#CField.__new__.__defaults__ = ('C', 10, 0, 0, 0)


class TDbField(dict):
    def __getattr__(self, aName: str):
        return self.get(aName)


class TDbFields(dict):
    Len = 0

    def Sort(self, aName = 'No'):
        return UArr.SortD(self, aName)


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

    def _RecRead(self):
        self._SeekRecNo()
        self.Buf = bytearray(self.Stream.read(self.RecLen))

    def _RecWrite(self):
        if (self.RecSave):
            self.RecSave = False
            self._SeekRecNo()
            return self.Stream.write(self.Buf)

    def _GetFieldData(self, aField: TDbField) -> bytearray:
        return self.Buf[aField.Ofst : aField.Ofst + aField.Len]

    def _SetFieldData(self, aField: TDbField, aData: bytearray):
        self.RecSave = True
        if (aField.Ofst + len(aData) >= len(self.Buf)):
            aData = aData[0:len(self.Buf) - aField.Ofst]
            Len = None
        else:
            Len = aField.Ofst + len(aData) - len(self.Buf)
        self.Buf[aField.Ofst:Len] = aData

    def Close(self): 
       if (self.Stream):
            self._RecWrite()
            self.Stream.close()
            self.Stream = None

    def GetSize(self) -> int:
        FileSize = self.Stream.seek(0, 2)
        return int((FileSize - self.HeadLen) / self.RecLen)

    def RecGo(self, aNo: int):
        self._RecWrite()
        if (aNo >= 0):
            self.RecNo = min(aNo, self.GetSize())
        else:
            self.RecNo = max(0, self.GetSize() + aNo)
        self._RecRead()

    def RecAdd(self, aCnt = 1):
        self._RecWrite()

        self.Buf = bytearray(self.RecFill * self.RecLen)
        self.Stream.seek(0, 2)
        for Cnt in range(aCnt):
            self.Stream.write(self.Buf)
        self.RecNo = self.GetSize() - 1

    def Create(self, aName: str, aFields: TDbFields):
        self.Close()

        self.Stream = open(aName, 'wb+')
        self._StructWrite(aFields)
        self._StructRead()

    def Open(self, aName: str, aROnly = False):
        self.Close()

        Mode = 'rb' if aROnly else 'rb+'
        self.Stream = open(aName, Mode)
        self._StructRead()

        self.RecGo(0)
