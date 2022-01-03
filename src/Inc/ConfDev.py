'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.01.03
License:     GNU, see LICENSE for more details
Description:
'''


import os
import json
#
from Inc.Log import Log


class TConfDev(dict):
    def __getattr__(self, aName: str):
        return self.get(aName)

    def _Replace(self, aData: str, aVars: dict) -> str:
        Delim = '%'
        #Items = re.findall(Macro + '(.*?)' + Macro, aData)
        Items = aData.split(Delim)[1::2]
        for Item in Items:
            Repl = aVars.get(Item)
            if (Repl is not None):
                aData = aData.replace(Delim + Item + Delim, str(Repl))
        return aData

    def Load(self, aDirConf: str, aVars: dict = {}):
        for File in sorted(os.listdir(aDirConf)):
            if (File.endswith('.json')):
                with open(aDirConf + '/' + File) as F:
                    Data = self._Replace(F.read(), aVars)
                    try:
                        Data = json.loads(Data)
                        for Item in Data.get('Dev', []):
                            Class = Item['Class']
                            Mod = __import__(Item['Module'], None, None, [Class])
                            TClass = getattr(Mod, Class)
                            self[Item['Alias']] = TClass(** Item['Param'])
                    except Exception as E:
                        Log.Print(1, 'x', 'Load()', E)
    '''
    def Clear(self):
         for Item in list(self.keys()):
            del self[Item]
    '''
