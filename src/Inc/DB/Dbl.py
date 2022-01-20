'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:

import os, time
from Inc.DB.Dbl import TDbl, TDblFields

dbl = TDbl()
File = 'Products.dbl'
if (os.path.isfile(File)):
    dbl.Open(File)
    for RecNo in dbl:
        lt = time.localtime(dbl.GetField('Created'))
        DateTime = '%d-%02d-%02d %02d:%02d:%02d' % (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])
        print(RecNo, dbl.GetField('Name'), DateTime, dbl.GetField('Votes'), dbl.GetField('Price'), dbl.GetField('Active'))
else:
    # see python struct format. https://docs.python.org/3/library/struct.html
    DblFields = TDblFields()
    DblFields.Add('Name', 's', 20)
    DblFields.Add('Created', 'f')
    DblFields.Add('Votes', 'i')
    DblFields.Add('Price', 'f')
    DblFields.Add('Active', '?')

    dbl.Create(File, DblFields)
    for Idx in range(10):
        dbl.RecAdd()
        dbl.SetField('Name', 'Monitor_%s' % Idx)
        dbl.SetField('Created', time.time())
        dbl.SetField('Votes', 10 + Idx)
        dbl.SetField('Price', 100.14 + Idx)
        dbl.SetField('Active', (Idx % 2) == 0)

        print('Added record', Idx)
        time.sleep(0.1)
dbl.Close()
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
        aName = aName.upper()

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
        self.S.seek(0)
        self.S.write(Data)

        self.S.seek(16)
        for K, V in aFields.Sort():
            Data = struct.pack('<11s1s1B3s', V.Name.encode(), V.Type.encode(), V.Len, b'\x00')
            self.S.write(Data)

    def _StructRead(self):
        self.Fields = TDblFields()

        self.S.seek(0)
        Data = self.S.read(16)
        Sign, self.HeadLen, self.RecLen, Fields = struct.unpack('<1B1H1H1H', Data[0:1+2+2+2])
        assert Sign == self.Sign, 'bad signature'

        for i in range(Fields):
            Data = self.S.read(16)
            FName, FType, FLen, X = struct.unpack('<11s1s1B3s', Data)
            Name = FName.split(b'\x00', 1)[0].decode()
            self.Fields.Add(Name, FType.decode(), FLen)
