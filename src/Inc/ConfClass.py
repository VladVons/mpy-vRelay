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
from Inc.Conf import TConfD


class TConfClass(TConfD):
    def __init__(self, aFile: str, aConf: TConfD = {}):
        super().__init__(aFile)
        self.Conf = aConf

    def _Replace(self, aData: str) -> str:
        Delim = '%'
        #Items = re.findall(Macro + '(.*?)' + Macro, aData)
        Items = aData.split(Delim)[1::2]
        for Item in Items:
            Repl = self.Conf.get(Item)
            if (Repl is not None):
                aData = aData.replace(Delim + Item + Delim, str(Repl))
        return aData

    def _Load(self, aFile: str):
        with open(aFile) as hF:
            Data = self._Replace(hF.read())
            try:
                Data = json.loads(Data)
                for Item in Data.get('Classes', []):
                    Class = Item.get('Class')
                    Param = Item.get('Param', {})
                    Module = Item.get('Module')
                    Mod = __import__(Module, None, None, [Class])
                    TClass = getattr(Mod, Class)
                    Obj = TClass(** Param)
                    Obj.Descr = Item.get('Descr', '')
                    self[Item['Alias']] = Obj
            except Exception as E:
                Log.Print(1, 'x', '_Load()', E)
                print('Data', Data)

    '''
     def _DirList(self, aDir):
        return [aDir + '/' + File for File in sorted(os.listdir(aDir)) if File.endswith('.json')]

    def Loads(self, aFiles: list, aVars: dict = {}):
        for File in aFiles:
            self.Load(File)

    def LoadDir(self, aDir: str, aVars: dict = {}):
        self.Loads(self._DirList(aDir), aVars)

    def LoadPlugin(self, aDir: str, aPlugin: list, aVars: dict = {}):
        DirList = self._DirList(aDir)
        Files = [DL for DL in DirList if any(P in DL for P in aPlugin)]
        self.Loads(Files, aVars)

    def Clear(self):
         for Item in list(self.keys()):
            del self[Item]
'''