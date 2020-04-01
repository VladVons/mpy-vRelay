'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
Description:.
'''


class TMenu():
    def AskYN(self, aMsg):
        Str = input('%s ?  Y/n:' % aMsg).lower()
        return (Str == 'y')

    def Parse(self, aPath: str, aItems: list):
        while True:
            print()
            print('Menu:', aPath)

            for Idx, Item in enumerate(aItems, 1):
                Key = list(Item.keys())[0]
                print(Idx, Key)

            if (aItems):
                print(0, 'Exit []')
                Str = input('Enter choice: ')
                if (len(Str) == 0):
                    break

                if (len(Str) == 1):
                    Idx = ord(Str[0]) - ord('0')
                    if (Idx == 0):
                        break
                    elif (Idx <= len(aItems)):
                        Item = aItems[Idx - 1]
                        Key  = list(Item.keys())[0]
                        Func = Item[Key]
                        if (Func):
                            Func(aPath + '/' + Key)
            else:
                input('Press ENTER to continue ...')
                break

    def Input(self, aItems: dict, aDef: dict = {}) -> dict:
        R = {}

        Title = list(aItems.keys())[0]
        print()
        print('-', Title, '-')

        Items = aItems[Title]
        for Idx, Item in enumerate(Items, 1):
            Name, Text, ValDef = Item

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
