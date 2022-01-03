'''
Author:      Vladimir Vons, Oster Inc.
Created:     2022.01.02
License:     GNU, see LICENSE for more details
Description:
'''


from .Sen import TSen
from Inc.Cron import IsNow


class TSen_cron(TSen):
    #Data = [('*/2 8-13 * * *', 22), ('* 14-23 * * *', 24)]
    Data = []

    def Init(self, aData: list):
        self.Data = aData

    async def Read(self):
        for Cron, Val in self.Data:
            if (IsNow(Cron)):
                return Val
