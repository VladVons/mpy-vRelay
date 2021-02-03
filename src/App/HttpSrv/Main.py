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
from Inc.Util import UStr, UFS, UHttp
from Inc.HttpSrv import THttpApi, THeader
from App.Utils import Reset


class THttpApiApp(THttpApi):
    DirApiCore = 'Inc/Api'
    DirApiUser = 'Plugin/Api'

    async def DoUrl(self, aWriter: asyncio.StreamWriter, aPath: str, aQuery: dict, aData: bytearray) -> str:
        #print('--- aPath', aPath, 'aQuery', aQuery, 'aData', aData)
        R = 'DoUrl()'

        Name, Ext = UStr.SplitPad(2, aPath.split('/')[-1], '.')
        if (Ext == 'py'):
            try:
                if (UFS.FileExists(self.DirApiUser + aPath)):
                    Dir = self.DirApiUser
                else:
                    Dir = self.DirApiCore
                #Lib = __import__((self.DirApi + '/' + Name).replace('/', '.'), None, None, ['TApi'])
                Lib = __import__(Dir + '/' + Name)
                R = await Lib.TApi().Query(aQuery)
                R = json.dumps(R) + '\r\n'
            except Exception as E:
                R = Log.Print(1, 'x', 'DoUrl()', E)

            Header = THeader()
            Header.Create(200, 'json', len(R))
            await aWriter.awrite(str(Header))
            await aWriter.awrite(R)

        elif (aPath == '/generate_204'):
            await self.LoadFile(aWriter, aPath + '.html', aQuery, aData)
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)

        elif (aPath == '/login'):
            if (aData):
                Query = self.ParseQuery(aData.decode('utf-8'))
                Conf['STA_ESSID'] = Query.get('_STA_ESSID')
                Conf['STA_Paswd'] = Query.get('_STA_Paswd')
                Conf.Save()
                Reset()

        elif (aPath == '/upload'):
            if (aData):
                Data = UHttp.UrlPercent(aData)
                print('--Data', Data)

                Pairs = Data.split('&')
                for Pair in Pairs:
                    Key, Value = Pair.split('=')
                    print(Key, Value)
        else:
            await self.LoadFile(aWriter, aPath, aQuery, aData)
