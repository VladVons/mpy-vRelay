#!/usr/bin/python3
# VladVons

import time
import socket
import asyncio as asyncio
import random


class TAScan():
    async def Scanner(self, aIP: str, aPort: int):
        Conn = asyncio.open_connection(aIP, aPort)
        try:
            Reader, Writer = await asyncio.wait_for(Conn, timeout = 0.5)
            print("{}:{} ok".format(aIP, aPort))
        except asyncio.TimeoutError:
            pass
        except Exception as E:
            #print('{}:{} err'.format(aIP, aPort))
            pass

    def Scan(self, aIP: list, aPort: list):
        Tasks = [self.Scanner(IP, Port) for IP in aIP for Port in aPort]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(Tasks))


class TScan():
    def IsOpen(self, aIP: str, aPort: int):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(0.01)
        try:
            Sock.connect((aIP, aPort))
            Sock.close()
            print("{}:{} ok".format(aIP, aPort))
        except:
            pass

    def Scan(self, aIP: list, aPort: list):
        for IP in aIP:
            for Port in aPort:
                self.IsOpen(IP, Port)



IP   = ["192.168.2.{}".format(i) for i in range(0, 255)]
Port = [21, 22, 80, 443, 3389, 8080]

Now = time.time()
Obj = TAScan()
Obj.Scan(IP, Port)
print('time is', round(time.time() - Now, 1))
print()

Now = time.time()
Obj = TScan()
#Obj.Scan(IP, Port)
print('time is', round(time.time() - Now, 1))
