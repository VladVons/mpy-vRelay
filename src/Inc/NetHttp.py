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
from .Task import TTask


class THttpApi():
    DirRoot = '/Web'
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
 
    def LoadFile(self, aPath: str, aQuery: str, aData: bytearray) -> str:
        if (aPath == '/'):
            aPath = self.FIndex

        if (UFS.FileExists(self.DirRoot + aPath)):
            Path = aPath
        else:
            Log.Print(1, 'e', 'File not found %s' % self.DirRoot + aPath)
            Path = self.F404

        Ext = Path.split('.')[-1]
        if (Ext in ['html', 'txt', 'css', 'json']):
            Mode = 'r'
        else:
            Mode = 'rb'
        return UFS.FileLoad(self.DirRoot + Path, Mode)


    async def ParseUrl(self, aPath: str, aQuery: str, aData: bytearray) -> str:
        if ('=' in aQuery):
            Query = dict(Pair.split('=') for Pair in aQuery.split('&'))
        else:
            Query = dict()

        Obj = UObj.GetAttr(self, self.GetMethod(aPath))
        if (Obj):
            R = await Obj(Query, aData)
        else:
            R = await self.DoUrl(aPath, Query, aData)
        return R

    async def DoUrl(self, aPath: str, aQuery: dict, aData: bytearray):
        return self.LoadFile(aPath, aQuery, aData)


class TTaskHttpServer(TTask):
    def __init__(self, aApi: THttpApi):
        self.Api = aApi

    async def CallBack(self, aReader: asyncio.StreamReader, aWriter: asyncio.StreamWriter):
        R = await UHttp.ReadHead(aReader, True)
        Len = int(R.get('content-length', '0'))
        if (Len > 0):
            R['content'] = await aReader.read(Len)
 
        try:
            await aWriter.awrite("HTTP/1.0 200 OK\r\n\r\n")
            Data = await self.Api.ParseUrl(R['path'], R['query'], R.get('content'))

            # ToDo. When many requests got exception:  OSError: [Errno 104] ECONNRESET
            await aWriter.awrite("%s\r\n" % Data)
            await aWriter.aclose()
        except Exception as E:
            Data = Log.Print(1, 'x', 'CallBack()', E)

    async def Run(self):
        #No need internal loop
        #await super().Run()

        return await asyncio.start_server(self.CallBack, "0.0.0.0", 80)
