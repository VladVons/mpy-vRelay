'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:.
'''

from Inc.Util import UArr


class TDbField(dict):
    def __getattr__(self, aName: str):
        return self.get(aName)

    def ValueToData(self, aValue) -> bytearray:
        raise NotImplementedError()

    def DataToValue(self, aValue: bytearray):
        raise NotImplementedError()
 

class TDbFields(dict):
    Len = 0

    def Add(self, aName: str, aType: str, aLen: int):
        raise NotImplementedError()

    def Sort(self, aName = 'No'):
        return UArr.SortDD(self, aName)

    def Get(self, aName: str) -> TDbField:
        R = self.get(aName)
        assert R, 'Field not found %s' % aName
        return R


class TDb():
    def __init__(self):
        self.Stream  = None
        self.HeadLen = 0
        self.RecLen  = 0
        self.RecNo   = 0
        self.RecSave = False
        self.Buf     = bytearray()    
        self.BufFill = b'\x00'
        self.Fields  = TDbFields()

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
            self.Stream.write(self.Buf)
            self._DoRecWrite()

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

    def GetField(self, aName: str):
        Field = self.Fields.Get(aName.upper())
        Data = self._GetFieldData(Field)
        return Field.DataToValue(Data)

    def SetField(self, aName: str, aValue):
        Field = self.Fields.Get(aName.upper())
        Value = Field.ValueToData(aValue)
        self._SetFieldData(Field, Value)

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

        self.Buf = bytearray(self.BufFill * self.RecLen)
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

        #self.HeadLen, self.RecLen
        self._StructRead()

        self.RecGo(0)

    def Close(self):
       if (self.Stream):
            self._RecWrite()
            self.Stream.close()
            self.Stream = None

    def _StructRead(self):
        # init vars self.HeadLen, self.RecLen, self.Fields
        raise NotImplementedError()

    def _StructWrite(self, aFields: TDbFields):
        raise NotImplementedError()

    def _DoRecWrite(self):
        pass
