'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
'''


from App import ConfApp
from Inc.Menu import TMenu


class TMenuApp(TMenu):
    async def _ExecApi(self, aPath: str, aParam: list):
        Path = 'IncP.Api.' + aPath.split('/')[-1]
        Lib  = __import__(Path , None, None, ['TApi'])
        await self.Exec(Lib.TApi().Exec, aParam)

    async def _ExecObj(self, aPath: str, aParam: list):
        await self.Exec(aParam[0], aParam[1])

    async def MSetup(self, aPath: str, aParam: list):
        Vars = ConfApp.Keys()
        self._ShowTree(Vars)
        if (not await self.AskYN('Continue')):
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
            ConfApp.update(R)
            ConfApp.Save() 
            print('Saved')

    async def MApi(self, aPath: str, aParam: list):
        Func = self._ExecApi
        Items = [
            ['Sen_dht22',       Func, [14]],
            ['Sen_ds18b20',     Func, [14]],
            ['Sen_sht31',       Func, [5, 4]],
            ['= = =',           None, None],
            ['Sys_conf',        Func, []],
            ['Sys_date',        Func, []],
            ['Sys_info',        Func, []],
            ['Sys_mem',         Func, []],
            ['Sys_plugin',      Func, []],
            ['Sys_reset',       Func, []]
        ]
        await self.Parse(aPath, Items)

    async def MMisc(self, aPath: str, aParam: list):
        from App.ConnSTA.Main import TConnSTA
        ConnSTA = TConnSTA()

        Items = [
            ['connect',         self._ExecObj, [ConnSTA.Connector, []]]
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
