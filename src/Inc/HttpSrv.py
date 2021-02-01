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

# ToDo. Rebooting after a while. Cause: 10rst cause:2, boot mode:(3,7

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
        #await aWriter.awrite(F.read() + '\r\n' - OK, but cant upload big files
        #ToDo. When Captive OSError: [Errno 104] ECONNRESET
        with open(aName, aMode) as F:
            while True:
                Data = F.read(512)
                if (not Data):
                    break
                await aWriter.awrite(Data)
                await asyncio.sleep_ms(10)

    async def LoadFile(self, aWriter: asyncio.StreamWriter, aPath: str, aQuery: str, aData: bytearray):
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

    async def ParseUrl(self, aWriter: asyncio.StreamWriter, aPath: str, aQuery: str, aData: bytearray):
        if ('=' in aQuery):
            Query = dict(Pair.split('=') for Pair in aQuery.split('&'))
        else:
            Query = dict()

        Obj = UObj.GetAttr(self, self.GetMethod(aPath))
        if (Obj):
            await Obj(aWriter, Query, aData)
        else:
            await self.DoUrl(aWriter, aPath, Query, aData)

    async def DoUrl(self, aWriter: asyncio.StreamWriter, aPath: str, aQuery: dict, aData: bytearray):
        await self.LoadFile(aWriter, aPath, aQuery, aData)

    async def CallBack(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter):
        R = await UHttp.ReadHead(aReader, True)
        Len = int(R.get('content-length', '0'))
        if (Len > 0):
            R['content'] = await aReader.read(Len)
 
        try:
            await self.ParseUrl(aWriter, R['path'], R['query'], R.get('content'))
            await aWriter.aclose()
        except Exception as E:
            Data = Log.Print(1, 'x', 'CallBack()', E)

    async def Run(self, aPort = 80):
        await asyncio.start_server(self.CallBack, "0.0.0.0", aPort)
