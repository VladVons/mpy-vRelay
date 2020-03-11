# ToDo. < 3.7 doesnt supports defaults parameter. Need own TField
CField = collections.namedtuple('Field', ('Type', 'Len', 'LenD', 'No', 'Ofst'), defaults = ('C', 10, 0, 0, 0))
CField.__new__.__defaults__ = ('C', 10, 0, 0, 0)

---------

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
