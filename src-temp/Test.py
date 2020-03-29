#!/usr/bin/micropython
#!/usr/bin/python3


import time


class TTest1():
    pass

async def Task1():
    import uasyncio as asyncio

    Cnt = 0
    while True:
        Cnt += 1
        print('Task1', Cnt)

        gc.collect()
        print('mem_free Led', gc.mem_free())

        await asyncio.sleep(3)
 
def Test1():
    import uasyncio as asyncio
    from Inc import UHrd

    WDog = UHrd.TWDog(0, 10)

    Loop = asyncio.get_event_loop()
    Loop.create_task(Task1())
    Loop.run_forever()


def Connect(aESSID: str, aPassw: str, aCnt: int = 20) -> bool:
    import sys
    import network

    Obj = network.WLAN(network.STA_IF)
    R = Obj.isconnected()
    if (not R):
        Obj.active(True)
        Obj.connect(aESSID, aPassw)

        while (not Obj.isconnected()) and (aCnt > 0):
            sys.stdout.write('.')
            time.sleep(1)
            aCnt -= 1
        R = aCnt > 0

    print('Network', Obj.ifconfig())
    return R


def TestMem():
    print('')

    import gc
    print('mem_free', gc.collect(), gc.mem_free())

    import uasyncio
    print('mem_free', gc.collect(), gc.mem_free())

    import umqtt.simple
    print('mem_free', gc.collect(), gc.mem_free())


def TestDbf_Create():
    import time
    from Inc.DB.Dbf import TDbf, TDbfFields

    Fields = TDbfFields()
    Fields.Add('FChr', 'c', 15)
    Fields.Add('FNUM', 'n', 10, 2)
    Fields.Add('FDAT', 'D')
    Fields.Add('FLOG', 'L')

    Dbf = TDbf()
    Dbf.Create('test.dbf', Fields)
    for i in range(1000):
        if (i % 100 == 0):
            print(i)
        Dbf.RecAdd()
        Dbf.SetField('FCHr', 'Hello %s' % i)
        Dbf.SetField('FNUM', i)
        Dbf.SetField('FDAT', time.time())
        Dbf.SetField('FLOG', bool(i % 2))
    Dbf.Close()


def TestDbf_Open():
    from Inc.DB.Dbf import TDbf

    Dbf = TDbf()
    Dbf.Open('test.dbf')

    FName = 'FChr'
    for i in Dbf:
        if (not Dbf.RecDeleted()):
            if (i % 100 == 0):
                print(i, Dbf.GetField(FName))


def TestDbl_Create():
    from Inc.DB.Dbl import TDbl, TDblFields

    Fields = TDblFields()
    #Fields.Add('Fs', 's', 10)
    #Fields.Add('FB1', 'B')
    Fields.Add('Ff1', 'd')
    Fields.Add('Ff2', 'd')
    Fields.Add('Ff3', 'd')

    Dbl = TDbl()
    Dbl.Create('test.dbl', Fields)
    for i in range(8640):
        t1 = time.time()
        if (i % 100 == 0):
            print(i, type(t1), t1)
        Dbl.RecAdd()
        #Dbl.SetField('Fs', 'Hello')
        #Dbl.SetField('FI', 1234)
        Dbl.SetField('Ff1', t1)
        #Dbl.SetField('Ff2', t1)
        #Dbl.SetField('Ff3', t1)
        #Dbl.SetField('Fd', 1.2345678)
    Dbl.Close()


def TestDbl_Open():
    from Inc.DB.Dbl import TDbl

    Dbl = TDbl()
    Dbl.Open('test.dbl')

    for i in Dbl:
            if (i % 100 == 0):
                #print(i, 'Fs', Dbl.GetField('Fs'))
                print(i, 'Ff1', Dbl.GetField('Ff1'))


#TestDbf_Create()
#TestDbf_Open()
#
#TestDbl_Create()
#TestDbl_Open()



