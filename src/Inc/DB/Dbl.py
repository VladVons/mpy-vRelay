'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.03
License:     GNU, see LICENSE for more details
Description:.
'''

import re
import struct
import collections
#
from .Db import TDb


CField = collections.namedtuple('Field', ('Type', 'Len', 'No', 'Ofst'))


class TDbl(TDb):
    def _ReadFields(self, aPack, aFields):
        self.Fields = {}

        RegEx = re.compile(r'([0-9]+?[a-zA-Z]+)')
        Packs = RegEx.split(aPack.replace('<', ''))
        if (Packs):
            Packs = ' '.join(Packs).split()
            Fields = aFields.split(',')
            Ofst = 0
            for No, Pack in enumerate(Packs):
                Type = '<' + Pack
                Name = Fields[No]
                Len  = struct.calcsize(Type)
                self.Fields[Name] = CField(Type, Len, No, Ofst)
                Ofst += Len

        self.HeadLen = 32 * 2
        self.RecLen  = struct.calcsize(aPack)

    def _StructWrite(self, aPack: str, aFields: str):
        self.Stream.seek(0)
        self.Stream.write('{:32}'.format(aPack).encode())
        self.Stream.write('{:32}'.format(aFields).encode())

        self._ReadFields(aPack, aFields)

    def _StructRead(self):
        self.Stream.seek(0)
        Data = struct.unpack('>32s', self.Stream.read(32))
        Pack = Data[0].decode().strip()
        Data = struct.unpack('>32s', self.Stream.read(32))
        Fields = Data[0].decode().strip()

        self._ReadFields(Pack, aFields)

    def SetField(self, aName: str, aValue):
        self.RecSave = True

        Field = self.Fields[aName]
        print(type(Field.Type), Field.Type, type(aValue), aValue)
        Data = struct.pack(Field.Type, aValue)
        self.Buf[Field.Ofst : Field.Ofst + Field.Len] = Data
