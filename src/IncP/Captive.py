'''
Author:      Vladimir Vons, Oster Inc
Created:     2020.02.15
License:     GNU, see LICENSE for more details
Description:

https://ansonvandoren.com/posts/esp8266-captive-web-portal-part-1/
'''


import uasyncio as asyncio
import usocket as socket
import network
#
from .WLan import TWLan, GetMac


class TCaptive():
    @staticmethod
    def _GetAnswer(aIP: str, aData: bytearray) -> bytes:
        # ** create the answer header **
        # copy the ID from incoming request
        R = aData[:2]
        # set response flags (assume RD=1 from request)
        R += b"\x81\x80"
        # copy over QDCOUNT and set ANCOUNT equal
        R += aData[4:6] + aData[4:6]
        # set NSCOUNT and ARCOUNT to 0
        R += b"\x00\x00\x00\x00"

        # ** create the answer body **
        # respond with original domain name question
        R += aData[12:]
        # pointer back to domain name (at byte 12)
        R += b"\xC0\x0C"
        # set TYPE and CLASS (A record and IN class)
        R += b"\x00\x01\x00\x01"
        # set TTL to 60sec
        R += b"\x00\x00\x00\x3C"
        # set response length to 4 bytes (to hold one IPv4 address)
        R += b"\x00\x04"
        # now actually send the IP address as 4 bytes (without the "."s)
        R += bytes(map(int, aIP.split(".")))
        return R

    async def Run(self, aPassw: str, aSleep: float = 0.1):
        AP = await TWLan().EnableAP(True, aPassw)
        IP = AP.ifconfig()[0]

        Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Sock.setblocking(False)
        Sock.bind(('', 53))

        while True:
            try:
                Data, Addr = Sock.recvfrom(1024)
                Data = self._GetAnswer(IP, Data)
                Sock.sendto(Data, Addr)
                # here is the gateway to listen HTTP on /
            except: pass # timeout

            await asyncio.sleep(aSleep)
