'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
'''


from Inc.Menu import TMenu
from Inc.Conf import Conf


class TMenuApp(TMenu):
    def MSetup(self, aPath):
        R = {}
        Vars = Conf.Keys()

        Items = {'WiFi Access': [['STA_ESSID', 'SSID', 'oster.com.ua1'], ['STA_Paswd', 'Password*', '']]}
        R.update(self.Input(Items, Vars))
        Items = {'Mqtt Server': [['Mqtt_Host', 'Host', 'vpn2.oster.com.ua'], ['Mqtt_Login', 'Login', ''], ['Mqtt_Paswd', 'Password', '']]}
        R.update(self.Input(Items, Vars))

        if (self.AskYN('Save')):
            Conf.update(R)
            Conf.Save() 
            print('Saved')

    def MInfo(self, aPath):
        from Inc.Api.sys_info import TApi
        Data = TApi().Exec()
        print(Data)

    def MReboot(self, aPath):
        from Inc.Api.sys_reset import TApi
        TApi().Exec()

    def MMain(self, aPath):
        Items = [
            {'Info':   self.MInfo},
            {'Setup':  self.MSetup}, 
            {'---': None},
            {'Reboot': self.MReboot},
        ]
        self.Parse(aPath, Items)
