'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.30
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
'''


'''
#from Inc.Log import Log

class TApiBase():
    Param = [{}]

    def Query(self, aData: dict) -> dict:
        Params = []

        if (self.Param == [{}]):
            Keys1 = []
        else:
            Keys1 = [list(P.keys())[0] for P in self.Param]

        Keys2 = list(aData.keys())
        Diff  = set(Keys2) - set(Keys1)
        if (Diff):
            Msg = Log.Print(1, 'x', 'Query()', Diff, E)
            raise Exception(Msg)

        for Param in self.Param:
            for Key, Val in Param.items():
                ValData = aData.get(Key)
                if (ValData is None):
                    ValData = Val
                Params.append(ValData)

        if (Params):
            return self.Exec(*Params)
        else:
            return self.Exec()

    def Exec(self, *aParam) -> dict:
        pass
'''

class TApiBase():
    pass
