'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.03.31
License:     GNU, see LICENSE for more details
'''

import upip 
#
from .NetWLan import Connect
from .Conf import Conf


def Install(aName: str):
    Net = Connect(Conf.STA_ESSID, Conf.STA_Paswd, Conf.STA_Net)
    if (Net.isconnected()):
        upip.install(aName)
    else:
        print('Cant connect WiFi')
