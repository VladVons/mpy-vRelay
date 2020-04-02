'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''


import sys
import json
#
from Inc.Conf import Conf
from Inc.Log  import Log
from Inc.Util import UStr
from Inc.NetHttp import THttpApi
from .Utils   import Reset


class THttpApiApp(THttpApi):
    DirApi = 'Inc/Api'

    def DoUrl(self, aPath: str, aQuery: dict, aData: bytearray) -> str:
        print('--- aPath', aPath, 'aQuery', aQuery, 'aData', aData)
        R = 'DoUrl()'

        Name, Ext = UStr.SplitPad(2, aPath.split('/')[-1], '.')
        if (Ext == 'py'):
            try:
                #Lib = __import__((self.DirApi + '/' + Name).replace('/', '.'), None, None, ['TApi'])
                Lib = __import__(self.DirApi + '/' + Name)
                R = Lib.TApi().Query(aQuery)
                R = json.dumps(R)
            except Exception as E: 
                sys.print_exception(E)
                R = Log.Print(1, 'x', 'DoUrl()', E)

        elif (aPath == '/generate_204'):
            aPath += '.html'

            R = super().DoUrl(aPath, aQuery, aData)
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)
        elif (aPath == '/login'):
            Query = self.ParseQuery(aData.decode('utf-8'))
            Conf['STA_ESSID'] = Query.get('STA_ESSID')
            Conf['STA_Paswd'] = Query.get('STA_Paswd')
            Conf.Save()
            Reset()
        else:
            R = super().DoUrl(aPath, aQuery, aData)
        return R