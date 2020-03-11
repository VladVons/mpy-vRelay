'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.29
License:     GNU, see LICENSE for more details
Description:.
'''


import struct
import time
#
from .Db import TDb, TDbFields, TDbField


class TDbfField(TDbField):
    def DefLen(self, aType: str, aLen: int):
        if (aLen == 0):
            aLen = {'C': 10, 'N': 10, 'D': 8, 'L': 1}.get(aType, 0)
        return aLen

    def ValueToData(self, aValue) -> bytearray:
        if (self.Type == 'L'):
            aValue = 'T' if aValue else 'F'
        elif (self.Type == 'D'):
            lt = time.localtime(aValue)
            aValue = '%04d%02d%02d' % (lt[0], lt[1], lt[2])
        else:
            aValue = str(aValue)
        return aValue.encode()

    def DataToValue(self, aValue: bytearray):
        aValue = aValue.decode().strip()

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
    Sign = 3

    def __init__(self):
        super().__init__()
        self.BufFill = b' '

    def _StructRead(self):
        self.Stream.seek(0)
        Data = self.Stream.read(32)
        Sign, LUpd, RecCnt, self.HeadLen, self.RecLen = struct.unpack('<1B3s1I1H1H', Data[0:1+3+4+2+2])
        assert Sign == self.Sign, 'bad signature'

        self.Fields = TDbfFields()
        self.Fields.Add('Del', 'C', 1, 0)

        self.Stream.seek(32)
        while True:
            Data = self.Stream.read(32)
            if (Data[0] == 0x0D):
                break

            FName, FType, X, FLen, FLenD = struct.unpack('<11s1s4s1B1B', Data[0:11+1+4+1+1])
            Name = FName.split(b'\x00', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen, FLenD)

    def _StructWrite(self, aFields: TDbfFields):
        RecLen  = aFields.Len + 1
        HeadLen = 32 + (32 * len(aFields)) + 1
        Data = struct.pack('<1B3B1I1H1H', self.Sign, 1, 1, 1, 0, HeadLen, RecLen)
        self.Stream.seek(0)
        self.Stream.write(Data)

        self.Stream.seek(32)
        for K, V in aFields.Sort():
            Data = struct.pack('<11s1s4s1B1B14s', V.Name.encode(), V.Type.encode(), b'\x00', V.Len, V.LenD, b'\x00')
            self.Stream.write(Data)
        self.Stream.write(b'\x0D')

    def _DoRecWrite(self):
        # YYMMDD, RecCount
        Data = struct.pack('<1B1B1B1I', 20, 1, 1, self.GetSize())
        self.Stream.seek(1)
        self.Stream.write(Data)

    def RecDelete(self, aMode: bool = True):
        self.RecSave = True
        self.Buf[0] = 42 if aMode else 32

    def RecDeleted(self):
        return self.Buf[0] == 42
