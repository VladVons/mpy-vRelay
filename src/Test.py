#!/usr/bin/micropython
#!/usr/bin/python3


import sys
import select
import uasyncio as asyncio



def GetInputChr():
    R = ''
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        R = sys.stdin.read(1)
    return R


async def GetInputStr(aPrompt = ''):
    R = ''
    while True:
        K = GetInputChr()
        if (K):
            if (ord(K) == 10): # enter
                print()
                return R
            elif (ord(K) == 27): # esc
                return ''
            elif (ord(K) == 127): # bs
                R = R[:-1]
            else:
                R += K
        sys.stdout.write("%s%s\r" % (aPrompt, R))
        await asyncio.sleep(0.2)


async def Test1():
    while True:
        print('Test1')
        await asyncio.sleep(5)


async def Test2():
    S = ''
    while True:
        print('Test2')

        S = await GetInputStr('Prompt: ')
        print('input', S)


loop = asyncio.get_event_loop()
loop.create_task(Test1())
loop.create_task(Test2())
loop.run_forever()
