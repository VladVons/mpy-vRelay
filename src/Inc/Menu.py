'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.01
License:     GNU, see LICENSE for more details
Description:
'''

import uasyncio as asyncio
#
from Inc.Util.UHrd  import GetInputStr, GetInputChr
from .Task import TTask



class TMenu():
    async def AskYN(self, aMsg: str):
        Str = await GetInputStr('%s ?  Y/n:' % aMsg).lower()
        return (Str == 'y')

    async def WaitMsg(self, aMsg: str = '') -> str:
        return await GetInputStr('%s (Press ENTER) ' % aMsg)

    async def Parse(self, aPath: str, aItems: list):
        while True:
            print()
            print('Menu:', aPath)

            for Idx, (Name, Func, Param) in enumerate(aItems, 1):
                if (Param):
                    print('%2s %s %s' % (Idx, Name, Param))
                else:
                    print('%2s %s' % (Idx, Name))

            if (not aItems):
                await self.WaitMsg('No items')
                break

            print(' 0', 'Exit')
            Str = await GetInputStr('Enter choice: ')
            if (Str == '') or (Str == '0') or (not Str.isdigit()):
                break

            Idx = int(Str)
            if (Idx > len(aItems)):
                await self.WaitMsg('Out of range')
                continue
            else:
                Name, Func, Param = aItems[Idx - 1]
                if (Func):
                    await Func(aPath + '/' + Name, Param)

    async def Input(self, aItems: dict, aDef: dict = {}) -> dict:
        R = {}

        Title, Items = aItems
        print()
        print('-', Title, '-')

        for Idx, (Name, Text, ValDef) in enumerate(Items, 1):
            ValDef = aDef.get(Name, ValDef)
            Val = ''
            while Val == '':
                Val = await GetInputStr('%s/%s) %s [%s]:' % (Idx, len(Items), Text, ValDef))
                if (not Val):
                    if (Text[-1] != '*'):
                        Val = ValDef
                        break

            Type = type(ValDef).__name__
            if (Type == 'int'):
                Val = int(Val)
            elif (Type == 'float'):
                Val = float(Val)

            R[Name] = Val
        return R


class TTaskMenu(TTask):
    def __init__(self, aApi: TMenu, aKey: str):
        self.Api = aApi
        self.Key = aKey

    async def Run(self):
        #No need internal loop
        #await super().Run()

        Msg = 'Press `%s` to enter menu' % (self.Key)
        print(Msg)
        while True:
            await asyncio.sleep(0.2)
            Key = GetInputChr()
            if (Key == self.Key):
                await self.Api.MMain('/Main', [])
                print(Msg)
