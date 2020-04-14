'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
'''


from Inc.Menu import TMenu
from Inc.Conf import Conf
from Inc.Util.UObj import GetTree
from Inc.Util.UArr import SortLD


class TMenuApp(TMenu):
    def ShowTree(self, aData: dict):
        for Var in SortLD(GetTree(aData), 'Key'):
            print('%15s = %s' % (Var['Key'], Var['Val']))

    def MSetup(self, aPath: str, aParam: list):
        Vars = Conf.Keys()
        self.ShowTree(Vars)
        if (not self.AskYN('Cntinue')):
            return

        R = {}
        Items = ['WiFi Access', [
            ['STA_ESSID', 'SSID',      'oster.com.ua'], 
            ['STA_Paswd', 'Password*', '']]
        ]
        R.update(self.Input(Items, Vars))

        Items = ['Mqtt Server', [
            ['Mqtt_Host',  'Host',     'vpn2.oster.com.ua'], 
            ['Mqtt_Login', 'Login',    ''], 
            ['Mqtt_Paswd', 'Password', '']]
        ]
        R.update(self.Input(Items, Vars))

        self.ShowTree(R)
        if (self.AskYN('Save')):
            Conf.update(R)
            Conf.Save() 
            print('Saved')

    def ApiExec(self, aPath: str, aParam: list):
        Path = 'Inc.Api.' + aPath.split('/')[-1]
        Lib  = __import__(Path , None, None, ['TApi'])
        if (aParam):
            Data = Lib.TApi().Exec(*aParam)
        else:
            Data = Lib.TApi().Exec()
        self.ShowTree(Data)
        self.WaitMsg()

    def MApi(self, aPath: str, aParam: list):
        Func = self.ApiExec
        Items = [
            ['dev_bme280', Func, [5, 4]],
            ['dev_dht11',  Func, [14]],
            ['dev_dht22',  Func, [14]],
            ['dev_sht21',  Func, [5, 4]],
            ['dev_sht31',  Func, [5, 4]],
            ['gpio_read',  Func, [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16]],
            ['sys_info',   Func, []],
            ['sys_mem',    Func, []],
            ['sys_reset',  Func, []]
        ]
        self.Parse(aPath, Items)


    def MMain(self, aPath: str, aParam: list):
        Items = [
            ['Api',    self.MApi, []],
            ['Setup',  self.MSetup, []]
        ]
        self.Parse(aPath, Items)
