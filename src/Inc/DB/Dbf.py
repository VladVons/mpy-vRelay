'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.29
License:     GNU, see LICENSE for more details
Description:.
'''

import os
import struct
import collections
import time
#
from .Db import TDb


#CHead  = collections.namedtuple('Head',  ('Sign', 'RecCnt', 'LUpd', 'HeadLen', 'RecLen'))
# ToDO. 3.7 supports defaults parameter
#CField = collections.namedtuple('Field', ('Type', 'Len', 'LenD', 'No', 'Ofst'), defaults = ('C', 10, 0, 0, 0))
#CField.__new__.__defaults__ = ('C', 10, 0, 0, 0)
CField = collections.namedtuple('Field', ('Type', 'Len', 'LenD', 'No', 'Ofst'))


class TDbf(TDb):
    def __init__(self):
        super().__init__()
        self.RecFill = ' '

    def _WriteFields(self, aFields: list):
        self.Stream.seek(31)
        self.Stream.write(b'\0')
        self.Stream.readline(20)

        R = 0
        for K, V in aFields.items():
            print(V.Type)
            #V.Ofst = R
            R += V.Len 
        return R

    def _ReadFields(self):
        self.Fields = {}

        Ofst = 1
        self.Stream.seek(32)
        while True:
            Data = self.Stream.read(32)
            FName, FType, X, FLen, FLenD = struct.unpack('11s1s4s1B1B', Data[0:11+1+4+1+1])
            if (FName[0] == 13):
                break

            Name = FName.split(b'\0',1)[0].decode()
            self.Fields[Name] = CField(Type = FType.decode(), Len = FLen, LenD = FLenD, Ofst = Ofst, No = len(self.Fields))
            Ofst += FLen

    def _ReadHead(self):
        self.Stream.seek(0)
        Data = self.Stream.read(32)
        Sign, LUpd, RecCnt, self.HeadLen, self.RecLen = struct.unpack('1B3s1I1H1H', Data[0:1+3+4+2+2])

    def _StructRead(self):
        self._ReadHead()
        self._ReadFields()
 
    def RecDelete(self, aMode: bool):
        self.RecSave = True
        self.Buf[0] = 42 if aMode else 32

    def RecDeleted(self):
        return self.Buf[0] == 42

    def GetFieldData(self, aField: CField) -> bytearray:
        return self.Buf[aField.Ofst : aField.Ofst + aField.Len]

    def SetFieldData(self, aField: CField, aData: bytearray):
        self.RecSave = True
        if (aField.Ofst + len(aData) >= len(self.Buf)):
            aData = aData[0:len(self.Buf) - aField.Ofst]
            Len   = None
        else:
            Len  = aField.Ofst + len(aData) - len(self.Buf)
        self.Buf[aField.Ofst:Len] = aData

    def GetField(self, aName: str):
        Field = self.Fields[aName]
        R = self.GetFieldData(Field).decode().strip()

        if (Field.Type == 'N'):
            if (Field.LenD > 0):
                R = float(R if R != '' else '0.0')
            else:
                R = int(R if R != '' else '0')
        elif (Field.Type == 'F'):
            R = float(R if R != '' else '0.0')
        elif (Field.Type == 'L'):
            R = True if R == 'T' else False
        elif (Field.Type == 'D'):
            if (R == ''):
                R = '20000101'
            #R = time.mktime([int(R[0:4]), int(R[4:6]), int(R[6:8]), 0, 0, 0, 0, 0])
        return R

    def SetField(self, aName: str, aValue):
        Field = self.Fields[aName]
        self.SetFieldData(Field, aValue)

    def Create(self, aName: str, aFields: list):
        self.Name = aName
        self.Close()

        self.Stream = open(aName, 'wb+')
        self._WriteFields(aFields)

