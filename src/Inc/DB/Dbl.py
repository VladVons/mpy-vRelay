'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:.
'''


import struct
#
from .Db import TDb, TDbFields, TDbField


class TDblField(TDbField):
    def ValueToData(self, aValue) -> bytearray:
        if (self.Type == 's'):
            R = struct.pack('<%s%s' % (self.Len, self.Type), aValue.encode())
        else:
            R = struct.pack('<%s%s' % (1, self.Type), aValue)
        return R

    def DataToValue(self, aValue: bytearray):
        if (self.Type == 's'):
            Data = struct.unpack('<%s%s' % (self.Len, self.Type), aValue)
            R = Data[0].split(b'\x00', 1)[0].decode()
        else:
            Data = struct.unpack('<%s%s' % (1, self.Type), aValue)
            R = Data[0]
        return R


class TDblFields(TDbFields):
    def Add(self, aName: str, aType: str, aLen: int = 1):
        if (aType != 's'):
            aLen = 1
        Len = struct.calcsize('<%s%s' % (aLen, aType))

        R = TDblField()
        R.update({'Name': aName, 'Type': aType, 'Len': Len, 'No': len(self), 'Ofst': self.Len})
        self[aName] = R
        self.Len += Len
        return R

    def GetStruct(self):
        R = '<'
        for K, V in self.Sort():
            R += '%s%s' % (V.Len, V.Type)
        return R


class TDbl(TDb):
    Sign = 71

    def _StructWrite(self, aFields: TDblFields):
        HeadLen = 16 + (16 * len(aFields))
        Data = struct.pack('<1B1H1H1H', self.Sign, HeadLen, aFields.Len, len(aFields))
        self.Stream.seek(0)
        self.Stream.write(Data)

        self.Stream.seek(16)
        for K, V in aFields.Sort():
            Data = struct.pack('<11s1s1B3s', V.Name.encode(), V.Type.encode(), V.Len, b'\x00')
            self.Stream.write(Data)

    def _StructRead(self):
        self.Fields = TDblFields()

        self.Stream.seek(0)
        Data = self.Stream.read(16)
        Sign, self.HeadLen, self.RecLen, Fields = struct.unpack('<1B1H1H1H', Data[0:1+2+2+2])
        assert Sign == self.Sign, 'not a valid signature'

        for i in range(Fields):
            Data = self.Stream.read(16)
            FName, FType, FLen, X = struct.unpack('<11s1s1B3s', Data)
            Name = FName.split(b'\x00', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen)

    def GetField(self, aName: str):
        Field = self.Fields.Get(aName)
        Data  = self._GetFieldData(Field)
        return Field.DataToValue(Data)

    def SetField(self, aName: str, aValue):
        self.RecSave = True

        Field = self.Fields.Get(aName)
        Data  = Field.ValueToData(aValue)
        self._SetFieldData(Field, Data)
