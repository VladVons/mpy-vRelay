'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.30
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
'''



class TApiBase():
    Param = {}

    def Get(self, aData, aKey: str):
        Diff = set(list(aData.keys())) - set(list(self.Param.keys()))
        if (Diff):
            raise Exception('Unknown %s' % Diff)

        Def = self.Param.get(aKey)
        if (Def is None):
            raise Exception('Unknown param %s' % aKey)

        Val = aData.get(aKey)
        if (Val is None):
            Val = Def
        else:
            Type = type(Def).__name__
            if (Type == 'int'):
                Val = int(Val)
            elif (Type == 'float'):
                Val = float(Val)
            elif (Type == 'bool'):
                Val = bool(Val)
        return Val
