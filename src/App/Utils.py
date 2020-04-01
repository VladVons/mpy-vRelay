'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.30
License:     GNU, see LICENSE for more details
Description:.
'''


from Inc.Task import Tasks


def Reset(aSec: int = 0):
    Log.Print(1, 'i', 'Reset', aSec)
    UHrd.LedFlash(2, 3, 0.2)
    Tasks.Stop()
    UHrd.Reset(aSec)

