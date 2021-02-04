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

    async def DoUrl(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        Path = aHead['path']
        Query = self.ParseQuery(aHead['query'])
        LenData = int(aHead.get('content-length', '0'))
        #print('--DoUrl Head', aHead)

        Name, Ext = UStr.SplitPad(2, Path.split('/')[-1], '.')
        if (Ext == 'py'):
            try:
                if (UFS.FileExists(self.DirApiUser + Path)):
                    Dir = self.DirApiUser
                else:
                    Dir = self.DirApiCore
                #Lib = __import__((self.DirApi + '/' + Name).replace('/', '.'), None, None, ['TApi'])
                Lib = __import__(Dir + '/' + Name)
                R = await Lib.TApi().Query(Query)
                R = json.dumps(R) + '\r\n'
            except Exception as E:
                R = Log.Print(1, 'x', 'DoUrl()', E)

            await self.Answer(aWriter, 200, 'json', R)

        elif (Path == '/generate_204'):
            await self.LoadFile(aWriter, Path + '.html')
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)

        elif (Path == '/login'):
            if (LenData > 0):
                Data = await aReader.read(LenData)
                Query = self.ParseQuery(Data.decode('utf-8'))
                Conf['STA_ESSID'] = Query.get('_STA_ESSID')
                Conf['STA_Paswd'] = Query.get('_STA_Paswd')
                Conf.Save()
                Reset()

        elif (Path == '/upload'):
            if (LenData > 0):
                from .Upload import TMulUpload

                Ref = aHead.get('referer')
                if (Ref):
                    Url, QueryR = UStr.SplitPad(2, Ref, '?')
                    QueryR = self.ParseQuery(QueryR)
                    Dir = QueryR.get('path', '')
                else:
                    Dir = ''

                R = await TMulUpload().Upload(aReader, aHead, Dir)
                R = json.dumps(R) + '\r\n'
                await self.Answer(aWriter, 200, 'txt', R)
        else:
            await self.LoadFile(aWriter, Path)
