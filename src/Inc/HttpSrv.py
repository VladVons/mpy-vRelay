'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
#
from .Log  import Log
from .Util import UFS, UObj, UStr, UHttp

#https://github.com/peterhinch/micropython-samples/blob/master/resilient/README.md
# ToDo. Rebooting after a while. Cause:
#rst cause:2, boot mode:(3,7)
#rst cause:2, boot mode:(3,6)

class THeader(list):
    @staticmethod
    def GetHead(aCode: int) -> str:
        Arr = {
            200: 'OK',
            302: 'Redirect',
            400: 'Bad request',
            404: 'Not found'
        }
        return Arr.get(aCode, 'Unknown')

    @staticmethod
    def GetMime(aExt: str) -> str:
        Arr = {
            'html': 'text/html',
            'css':  'text/css',
            'js':   'text/javascript',
            'json': 'text/json',
            'png':  'image/png',
            'gif':  'image/gif',
            'jpg':  'image/jpeg',
            'ico':  'image/x-icon',
            'zip':  'application/zip'
        }
        return Arr.get(aExt, 'text/plain')

    def __str__(self):
        return '\r\n'.join(self)

    def Create(self, aCode, aType, aLen):
        self.clear()
        self.append('HTTP/1.1 %d %s' % (aCode, self.GetHead(aCode)))
        self.append('Content-Type: %s' % self.GetMime(aType))
        self.append('Server: MicroPy')
        self.append('Content-Length: %d' % aLen)
        self.append('\r\n')


class THttpApi():
    DirRoot = '/Plugin/Web'
    FIndex  = '/index.html'
    F404    = '/page_404.html'

    @staticmethod
    def GetMethod(aPath: str) -> str:
        return 'p' + aPath.replace('/', '_')

    @staticmethod
    def ParseQuery(aQuery: str) -> dict:
        R = {}
        for i in aQuery.split('&'):
            Key, Value = UStr.SplitPad(2, i, '=')
            R[Key] = Value
        return R

    @staticmethod
    async def FileToStream(aWriter: asyncio.StreamWriter, aName: str, aMode: str = 'r'):
        with open(aName, aMode) as F:
            while True:
                Data = F.read(512)
                if (not Data):
                    break
                await aWriter.awrite(Data)
                await asyncio.sleep_ms(10)

    @staticmethod
    async def Answer(aWriter: asyncio.StreamWriter, aCode: int, aType: str, aData):
        Header = THeader()
        Header.Create(aCode, aType, len(aData))
        await aWriter.awrite(str(Header))
        await aWriter.awrite(aData)

    async def LoadFile(self, aWriter: asyncio.StreamWriter, aPath: str):
        if (aPath == '/'):
            aPath = self.FIndex

        if (UFS.FileExists(self.DirRoot + aPath)):
            Path = aPath
            Code = 200
        else:
            Log.Print(1, 'e', 'File not found %s' % self.DirRoot + aPath)
            Path = self.F404
            Code = 404

        Ext = Path.split('.')[-1]
        if (Ext in ['html', 'txt', 'css', 'json']):
            Mode = 'r'
        else:
            Mode = 'rb'

        Header = THeader()
        Header.Create(Code, Ext, UFS.FileSize(self.DirRoot + Path))
        await aWriter.awrite(str(Header))
        await self.FileToStream(aWriter, self.DirRoot + Path, Mode)

    async def DoUrl(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter, aHead: dict):
        await self.LoadFile(aWriter, aHead['path'])

    async def CallBack(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter):
        Head = await UHttp.ReadHead(aReader, True)
        Log.Print(2, 'i', 'CallBack()', 'path: %s, query: %s' % (Head.get('path'), Head.get('query')))

        Method = self.GetMethod(Head.get('path'))
        Obj = UObj.GetAttr(self, Method)
        try:
            if (Obj):
                await Obj(aReader, aWriter, Head)
            else:
                await self.DoUrl(aReader, aWriter, Head)
            await aWriter.aclose()
        except Exception as E:
            Data = Log.Print(1, 'x', 'CallBack()', E)

    async def Run(self, aPort = 80):
        await asyncio.start_server(self.CallBack, "0.0.0.0", aPort)
