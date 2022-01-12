'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.01.12
License:     GNU, see LICENSE for more details
Description:
'''

import json
import uasyncio as asyncio
#
#from App import ConfApp
from IncP.BLE import TBLE
from Inc.Log  import Log
from Inc.Plugin import Plugin
from IncP.Marker import Marker


class TBleEx(TBLE):
    async def _DoPost(self, aOwner, aMsg):
        #print('TBleEx._DoPost', aOwner, aMsg)
        Data = Marker(self, aOwner, aMsg)
        print('TBleEx.Send', Data)
        self.Send(json.dumps(Data))

    def _DoConnect(self, aOn: bool, aAddr: bytes):
        # allow multiple connection
        if (aOn):
            self._Advertise()
 
        Info = {'On': aOn, 'Func': 'DoConnect'})
        self.Send(json.dumps(Info))
        #Plugin.PostSyn(self, Info)

    def _DoReceive(self, aMsg: str):
        print('DoReceive', aMsg)

    async def Run(self, aSleep: int = 5):
        Cnt = 0
        while True:
            Cnt += 1
            Msg = "TBleEx.Run %s\n" % (Cnt)
            self.Send(Msg)
            await asyncio.sleep(aSleep)
