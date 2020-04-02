#!/usr/bin/micropython
#!/usr/bin/python3

import gc
import time

#from Inc.Conf import Conf
#from App.Menu import TMenuApp
#Menu = TMenuApp()
#Menu.MMain('/Main', [])

#for i in range(1, 16):
#    print(hex(i)[-1])

from Inc.Util import UObj, UArr
#V1 = {'a1': 11, 'a2':12, 'c1': 31, 'b1':21}
V1 = {'a1': {'Key': 11, 'Val':111}, 'a2':{'Key': 2, 'Val': 222}, 'c1': {'Key': 4, 'Val': 444}, 'b1':{'Key': 3, 'Val': 333}}
#V1 = UObj.GetTree(V1)
#for i in V1:
#    print(i['Key'], i['Val'])

V1 = UArr.SortD(V1, 'Val')
for i in V1:
    #print(i['Key'], i['Val'])
    print(i)
