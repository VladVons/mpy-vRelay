'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:.
'''

import json
#
from Inc.Util import UStr, UFS
from Inc.Http.HttpSrv import THttpApi


class THttpApiApp(THttpApi):
    DirApiCore = 'Inc/Api'
    DirApiUser = 'Plugin/Api'

    async def p_upload(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        from .p_upload import DoUrl
        await DoUrl(self, aReader, aWriter, aHead)

    async def p_login(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        from .p_login import DoUrl
        await DoUrl(self, aReader, aWriter, aHead)

    async def DoUrl(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        Path = aHead['path']
        Query = self.ParseQuery(aHead['query'])

        Name, Ext = UStr.SplitPad(2, Path.split('/')[-1], '.')
        if (Ext == 'py'):
            if (UFS.FileExists(self.DirApiUser + Path)):
                Dir = self.DirApiUser
            else:
                Dir = self.DirApiCore
            Lib = __import__(Dir + '/' + Name)
            R = await Lib.TApi().Query(Query)
            R = json.dumps(R) + '\r\n'
            await self.Answer(aWriter, 200, 'json', R)

        elif (Path == '/generate_204'):
            await self.LoadFile(aWriter, Path + '.html')
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)

        else:
            await self.LoadFile(aWriter, Path)
