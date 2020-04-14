'''
Author:      Vladimir Vons, Oster Inc.
Created:     2020.04.03
License:     GNU, see LICENSE for more details
Description:.
'''

import socket


def CheckHostPort(aHost: str, aPort: str, aTimeOut: int = 1) -> bool:
    Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Sock.settimeout(aTimeOut)
    try:
        R = (Sock.connect_ex((aHost, aPort)) == 0)
        Sock.close()
    except:
        R = False
    return R
