'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.02.21
License:     GNU, see LICENSE for more details
Description:
'''

import os, machine


def MountSD(aDir: str = '/sd'):
    SD = machine.SDCard()
    os.mount(SD, aDir)
