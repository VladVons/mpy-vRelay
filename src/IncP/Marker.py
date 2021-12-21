'''
Author:      Vladimir Vons, Oster Inc
Created:     2021.03.05
License:     GNU, see LICENSE for more details
Description:.
'''

import machine
from ubinascii import hexlify
#
from App import ConfApp
from Inc.Util.UTime import GetDate, GetTime

def Marker(aSender, aOwner, aData):
    return {
        #'Sender': aSender.__class__.__name__,
        'Owner':  aOwner.__class__.__name__ ,
        'Id':     hexlify(machine.unique_id()).decode('utf-8'),
        'Alias':  ConfApp.Alias,
        'Date':   '%s %s'% (GetDate(), GetTime()),
        'Data':   aData
        }
