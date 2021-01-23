'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
Description:.
'''


class TMenu():
    def AskYN(self, aMsg: str):
        Str = input('%s ?  Y/n:' % aMsg).lower()
        return (Str == 'y')

    def WaitMsg(self, aMsg: str = '') -> str:
        return input('%s (Press ENTER) ' % aMsg)

    def Parse(self, aPath: str, aItems: list):
        while True:
            print()
            print('Menu:', aPath)

            for Idx, (Name, Func, Param) in enumerate(aItems, 1):
                if (Param):
                    print('%2s %s %s' % (Idx, Name, Param))
                else:
                    print('%2s %s' % (Idx, Name))

            if (not aItems):
                self.WaitMsg('No items')
                break

            print(' 0', 'Exit')
            Str = input('Enter choice: ')
            if (Str == '') or (Str == '0'):
                break

            Idx = int(Str)
            if (Idx > len(aItems)):
                self.WaitMsg('Out of range')
                continue
            else:
                Name, Func, Param = aItems[Idx - 1]
                if (Func):
                    Func(aPath + '/' + Name, Param)

    def Input(self, aItems: dict, aDef: dict = {}) -> dict:
        R = {}

        Title, Items = aItems
        print()
        print('-', Title, '-')

        for Idx, (Name, Text, ValDef) in enumerate(Items, 1):
            ValDef = aDef.get(Name, ValDef)
            Val = ''
            while Val == '':
                Val = input('%s/%s) %s [%s]:' % (Idx, len(Items), Text, ValDef))
                if (not Val):
                    if (Text[-1] != '*'):
                        Val = ValDef
                        break

            Type = type(ValDef).__name__
            if (Type == 'int'):
                Val = int(Val)
            elif (Type == 'float'):
                Val = float(Val)

            R[Name] = Val
        return R
