'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.06.18
License:     GNU, see LICENSE for more details
Description: micropython ESP8266
             DS1820 temperature sensor
'''
import binascii

from Inc.Dev.ds18b20 import DS1820
from Inc.Api import TApiBase
from Inc.Log import Log


class TApi(TApiBase):
    async def Exec(self, aPin: int, aIDs: list) -> dict:
        HexID = []
        for ID in aIDs:
            HexID.append(binascii.unhexlify(ID))

        R = []
        try:
            Obj = DS1820(aPin)
            Data = await Obj.Get(HexID)
            for Item in Data:
                R.append({'id':binascii.hexlify(Item['id']), 'value':Item['value']})
        except Exception as E:
            Log.Print(1, 'Err: dev_ds18b20', 'Api()', E)
        return R

    async def Query(self, aData: dict) -> dict:
        Pin = int(aData.get('pin', '14'))
        Id  = aData.get('id')
        if (Id):
            Arr = Id.split(',')
        else:
            Arr = []
        return await self.Exec(Pin, Arr)
