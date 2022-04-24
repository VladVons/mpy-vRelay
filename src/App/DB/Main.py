'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.01.19
License:     GNU, see LICENSE for more details
Description:

ampy --port /dev/ttyUSB0 --baud 115200 rm values.db
'''


import os
import time
import uasyncio as asyncio
#
from Inc.DB.Dbl import TDbl, TDblFields
from Inc.Util.UFS import FileExists
from IncP.Log import Log


class TDB():
    def __init__(self, aFile: str):
        self.File = aFile 

    async def _DoPost(self, aOwner, aMsg):
        if (aMsg.get('Val')):
            Log.Print(1, 'i', 'TDB._DoPost()', aMsg)

            db = self.Init(self.File)
            db.RecAdd()
            db.SetField('Alias', aMsg.get('Alias', 'X'))
            db.SetField('Time', time.time())
            db.SetField('Val', aMsg.get('Val'))
            db.Close()

    def Init(self, aFile):
        db = TDbl()
        if (FileExists(aFile)):
            db.Open(aFile)
        else:
            Fields = TDblFields()
            Fields.Add('Alias', 's', 5)
            Fields.Add('Time', 'f')
            Fields.Add('Val', 'f')
            db.Create(aFile, Fields)
        return db

    def Trunc(self, aFile):
        db1 = self.Init(aFile)
        if (db1.GetSize() < 60*24*7):
            db1.Close()
        else:
            db2 = TDbl()
            FileTmp = aFile + '.tmp'
            db2.Create(FileTmp, db1.Fields)
            db1.RecGo(60*24*1)
            for R in db1:
                db2.RecAdd()
                db2.SetRec(db1.Buf)
            db1.Close()
            db2.Close()

            os.remove(aFile)
            os.rename(FileTmp, aFile)

    async def Run(self, aSleep = 60):
        while True:
            self.Trunc(self.File)
            await asyncio.sleep(aSleep)
