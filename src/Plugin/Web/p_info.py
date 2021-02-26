'''
Author:      Vladimir Vons, Oster Inc.
Created:     2021.02.11
License:     GNU, see LICENSE for more details

Description:.http://IP/info
'''

import json
#
from IncP.Api.sys_info import TApi


class THttpApiEx():
    def __init__(self, aParent):
        self.Parent = aParent

    async def Query(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        R = await TApi().Query({})
        R = json.dumps(R) + '\r\n'
        await self.Parent.Answer(aWriter, 200, 'json', R)
