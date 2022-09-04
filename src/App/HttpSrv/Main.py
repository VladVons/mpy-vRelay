'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.10
License:     GNU, see LICENSE for more details
Description:
'''


import json
#
from Inc.Http.HttpSrv import THttpApi
from Inc.ApiParse import QueryToDict, QueryUrl


class THttpApiApp(THttpApi):
    async def p_upload(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        from .p_upload import DoUrl
        await DoUrl(self, aReader, aWriter, aHead)

    async def p_login(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        from .p_login import DoUrl
        await DoUrl(self, aReader, aWriter, aHead)

    async def DoUrl(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        Path = aHead['path']
        Query = QueryToDict(aHead['query'])
        print('-x. DoUrl() ', Path, Query)
        R = await QueryUrl(Path, Query)
        if (R):
            Type = Query.get('r', 'json')
            await self.Answer(aWriter, 200, Type, R)
        elif (Path == '/generate_204'):
            await self.LoadFile(aWriter, Path + '.html')
            #R = UStr.TDictRepl({'$SSID': 'mySSID'}).Parse(R)
        else:
            await self.LoadFile(aWriter, Path)
