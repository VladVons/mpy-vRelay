'''
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2021.02.28
License:     GNU, see LICENSE for more details
Description:
'''


from IncP.Log import TLog, TEchoConsole


class TEchoConsoleEx(TEchoConsole):
    def Write(self, aArgs: dict):
        aE = aArgs.get('aE')
        if (aE):
            sys.print_exception(aE)
        super().Write(aArgs)

Log = TLog()
