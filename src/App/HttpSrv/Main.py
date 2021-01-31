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
from Inc.Util import UStr, UFS
from Inc.NetHttp import THttpApi
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
                R = json.dumps(R)
            except Exception as E:
                R = Log.Print(1, 'x', 'DoUrl()', E)

            #ToDo. When many requests got exception:  OSError: [Errno 104] ECONNRESET
            await aWriter.awrite(R)

        elif (aPath == '/generate_204'):
            await self.LoadFile(aWriter, aPath + '.html', aQuery, aData)
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)

        elif (aPath == '/login'):
            if (aData):
                Query = self.ParseQuery(aData.decode('utf-8'))
                Conf['STA_ESSID'] = Query.get('STA_ESSID')
                Conf['STA_Paswd'] = Query.get('STA_Paswd')
                Conf.Save()
                Reset()

        else:
            await self.LoadFile(aWriter, aPath, aQuery, aData)
        return R
