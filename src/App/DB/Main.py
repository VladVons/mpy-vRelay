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


class TDB():
    def __init__(self):
        self.db = None

    async def _DoPost(self, aOwner, aMsg):
        if (self.db):
            if (aMsg.get('Val')):
                print('---x-TDB', aMsg, self.db.GetSize())

                self.db.RecAdd()
                self.db.SetField('Alias', aMsg.get('Alias', ''))
                self.db.SetField('Created', time.time())
                self.db.SetField('Value', aMsg.get('Val', 0))

    def Init(self, aFile):
        self.db = TDbl()
        if (FileExists(aFile)):
            self.db.Open(aFile)
        else:
            Fields = TDblFields()
            Fields.Add('Alias', 's', 8)
            Fields.Add('Created', 'f')
            Fields.Add('Value', 'f')
            self.db.Create(aFile, Fields)

    def Trunc(self, aFile):
        if (self.db.GetSize() > 10000):
            db = TDbl()
            db.Create(File + '.tmp', self.db.Fields)
            self.db.RecGo(1000)
            for RecNo in self.db:
                db.RecAdd()
                db.SetRec(self.db.Buf)
            db.Close()

            self.db.Close()
            os.rename(File + '.tmp', aFile)
            self.Init(aFile)

    async def Run(self, aFile):
        self.Init(aFile)

        while True:
            self.Trunc(aFile)
            await asyncio.sleep(60)
