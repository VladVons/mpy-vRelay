'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2018.04.25
License:     GNU, see LICENSE for more details
Description:
'''


from Inc.Dev.mhz19 import MHZ19
from Inc.Api import TApiBase


class TApi(TApiBase):
    def Exec(self, aPort: int, aSpeed: int) -> dict:
        try:
            Obj = MHZ19(aPort, aSpeed)
            R = Obj.GetCO2()
        except Exception as E:
            R = None
        return {'co2': R}

    def Query(self, aData: dict) -> dict:
        aPort  = int(aData.get('port', '1'))
        aSpeed = int(aData.get('speed', '9600'))
        return self.Exec(aPort, aSpeed)
