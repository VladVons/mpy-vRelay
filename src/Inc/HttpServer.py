'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:.
'''

import uasyncio as asyncio
#
from Inc.Log import Log
from Inc import UFS, UObj
from Inc.UStr import SplitPad


class THttpApi():
    def __init__(self):
        self.RootDir = '/Web'
        self.FIndex  = '/index.html'
        self.F404    = '/page_404.html'

    @staticmethod
    def GetMethod(aPath: str) -> str:
        return 'p' + aPath.replace('/', '_')

    @staticmethod
    def ParseQuery(aQuery: str) -> dict:
        R = {}
        for i in aQuery.split('&'):
            Key, Value = SplitPad(2, i, '=')
            R[Key] = Value
        return R
 
    def LoadFile(self, aPath: str, aQuery: str, aData: str) -> str:
        if (aPath == '/'):
            aPath = self.FIndex

        if (UFS.FileExists(self.RootDir + aPath)):
            Path = aPath
        else:
            Log.Print(1, 'File not found %s' % self.RootDir + aPath)
            Path = self.F404

        Ext = Path.split('.')[-1]
        if (Ext in ['html', 'txt', 'css']):
            Mode = 'r'
        else:
            Mode = 'rb'
        return UFS.FileLoad(self.RootDir + Path, Mode)

 
    def ParseUrl(self, aPath: str, aQuery: str, aData: str) -> str:
        Obj = UObj.GetAttr(self, self.GetMethod(aPath))
        if (Obj):
            R = Obj(aQuery, aData)
        else: 
            R = self.DoUrl(aPath, aQuery, aData)
        return R

    def DoUrl(self, aPath, aQuery, aData):
        return self.LoadFile(aPath, aQuery, aData)


class THttpServer():
    def __init__(self, aApi: THttpApi):
        self.Api = aApi

    async def CallBack(self, aReader, aWriter):
        R = {}
        while True:
            Data = await aReader.readline()
            if (Data == b'\r\n'):
                break

            Data = Data.decode('utf-8').strip()
            if (len(R) == 0):
                R['mode'], R['url'], R['prot'] = SplitPad(3, Data, ' ')
                R['path'], R['query'] = SplitPad(2, R['url'], '?')
            else:
                Key, Value = SplitPad(2, Data, ':')
                R[Key.lower()] = Value.strip()

        Len = int(R.get('content-length', '0'))
        if (Len > 0):
            R['content'] = await aReader.read(Len)

        await aWriter.awrite("HTTP/1.0 200 OK\r\n\r\n")
        Data = self.Api.ParseUrl(R['path'], R['query'], R.get('content'))
        await aWriter.awrite("%s\r\n" % Data)
        await aWriter.aclose()

    async def Run(self, aPort: int = 80):
        return await asyncio.start_server(self.CallBack, "0.0.0.0", aPort)
