#!/usr/bin/micropython
#!/usr/bin/python3

import gc
import time

from Inc.Conf import Conf
from App.Menu import TMenuApp
Menu = TMenuApp()
Menu.MMain('/Main', [])

#for i in range(1, 16):
#    print(hex(i)[-1])
