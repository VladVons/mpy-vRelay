'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
'''


from Inc.Menu import TMenu
from Inc.Conf import Conf


class TMenuApp(TMenu):
    async def _ExecApi(self, aPath: str, aParam: list):
        Path = 'Inc.Api.' + aPath.split('/')[-1]
        Lib  = __import__(Path , None, None, ['TApi'])
        await self.Exec(Lib.TApi().Exec, aParam)

    async def _ExecObj(self, aPath: str, aParam: list):
        await self.Exec(aParam[0], aParam[1])

    async def MSetup(self, aPath: str, aParam: list):
        Vars = Conf.Keys()
        self._ShowTree(Vars)
        if (not await self.AskYN('Cntinue')):
            return

        R = {}
        Items = ['WiFi Access', [
            ['STA_ESSID', 'SSID',      'oster.com.ua'], 
            ['STA_Paswd', 'Password*', '']]
        ]
        R.update(await self.Input(Items, Vars))

        Items = ['Mqtt Server', [
            ['Mqtt_Host',  'Host',     'vpn2.oster.com.ua'], 
            ['Mqtt_Port',  'Port',     1883],
            ['Mqtt_Login', 'Login',    ''], 
            ['Mqtt_Paswd', 'Password', '']]
        ]
        R.update(await self.Input(Items, Vars))

        self._ShowTree(R)
        if (await self.AskYN('Save')):
            Conf.update(R)
            Conf.Save() 
            print('Saved')

    async def MApi(self, aPath: str, aParam: list):
        Func = self._ExecApi
        Items = [
            ['dev_dht22',       Func, [14]],
            ['dev_ds18b20',     Func, [14]],
            ['dev_sht31',       Func, [5, 4]],
            ['---',             None, None],
            ['sys_conf',        Func, []],
            ['sys_info',        Func, []],
            ['sys_mem',         Func, []],
            ['sys_plugin',      Func, []],
            ['sys_reset',       Func, []]
        ]
        await self.Parse(aPath, Items)

    async def MMisc(self, aPath: str, aParam: list):
        from App.Utils import TWLanApp
        WLanApp = TWLanApp()

        Items = [
            ['connect',         self._ExecObj, [WLanApp.TryConnect, []]]
        ]
        await self.Parse(aPath, Items)

    async def MMain(self, aPath: str, aParam: list):
        Items = [
            ['Api',    self.MApi, []],
            ['Misc',   self.MMisc, []],
            ['Setup',  self.MSetup, []]
        ]
        await self.Parse(aPath, Items)

    async def DoRun(self):
        await self.MMain('/Main', [])
