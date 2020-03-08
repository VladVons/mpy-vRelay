'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.29
License:     GNU, see LICENSE for more details
Description:.
'''


import struct
#
from .Db import TDb, TDbFields, TDbField


class TDbfField(TDbField):
    def DefLen(self, aType: str, aLen: int):
        if (aLen == 0):
            aLen = {'C': 10, 'N': 10, 'D': 8, 'L': 1}.get(aType, 0)
        return aLen

    def DefValue(self, aValue: str):
        if (self.Type == 'N'):
            if (self.LenD > 0):
                aValue = float(aValue if aValue != '' else '0.0')
            else:
                aValue = int(aValue if aValue != '' else '0')
        elif (self.Type == 'F'):
            aValue = float(aValue if aValue != '' else '0.0')
        elif (self.Type == 'L'):
            aValue = True if aValue == 'T' else False
        elif (self.Type == 'D'):
            if (aValue == ''):
                aValue = '20010101'
            #R = time.mktime([int(R[0:4]), int(R[4:6]), int(R[6:8]), 0, 0, 0, 0, 0])
        return aValue


class TDbfFields(TDbFields):
    def Add(self, aName: str, aType: str, aLen: int = 0, aLenD: int = 0):
        aName = aName.upper()
        aType = aType.upper()

        R = TDbfField()
        aLen = R.DefLen(aType, aLen)
        R.update({'Name': aName, 'Type': aType, 'Len': aLen, 'No': len(self), 'Ofst': self.Len, 'LenD': aLenD})
        self[aName] = R
        self.Len += aLen
        return R


class TDbf(TDb):

    def __init__(self):
        super().__init__()
        self.RecFill = b' '

    def _StructRead(self):
        self._ReadHead()
        self._ReadFields()

    def _StructWrite(self, aFields: TDbfFields):
        RecLen  = aFields.Len + 1
        HeadLen = 32 + (32 * len(aFields)) + 1
        Data = struct.pack('<1B3B1I1H1H', 3, 1, 1, 1, 0, HeadLen, RecLen)
        self.Stream.seek(0)
        self.Stream.write(Data)

        self.Stream.seek(32)
        for K, V in aFields.Sort():
            Data = struct.pack('<11s1s4s1B1B14s', V.Name.encode(), V.Type.encode(), b'\x00', V.Len, V.LenD, b'\x00')
            self.Stream.write(Data)
        self.Stream.write(b'\x0D')

    def _ReadFields(self):
        self.Fields = TDbfFields()
        self.Fields.Add('Del', 'C', 1, 0)

        self.Stream.seek(32)
        while True:
            Data = self.Stream.read(32)
            if (Data[0] == 0x0D):
                break

            FName, FType, X, FLen, FLenD = struct.unpack('<11s1s4s1B1B', Data[0:11+1+4+1+1])
            Name = FName.split(b'\0', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen, FLenD)

    def _ReadHead(self):
        self.Stream.seek(0)
        Data = self.Stream.read(32)
        Sign, LUpd, RecCnt, self.HeadLen, self.RecLen = struct.unpack('<1B3s1I1H1H', Data[0:1+3+4+2+2])

    def RecDelete(self, aMode: bool = True):
        self.RecSave = True
        self.Buf[0] = 42 if aMode else 32

    def RecDeleted(self):
        return self.Buf[0] == 42

    def GetField(self, aName: str):
        Field = self.Fields[aName.upper()]
        R = self.GetFieldData(Field).decode().strip()
        return Field.DefValue(R)

    def SetField(self, aName: str, aValue):
        Field = self.Fields[aName.upper()]
        self.SetFieldData(Field, aValue.encode())
