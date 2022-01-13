'''
Author:      Vladimir Vons, Oster Inc
Created:     2022.01.11
License:     GNU, see LICENSE for more details
Description:

https://mpython.readthedocs.io/en/master/library/micropython/ubluetooth.html
'''


import bluetooth
from micropython import const
from ubinascii import hexlify
import struct
#
from Inc.Log  import Log


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# support 'Heart Rate'
_HR_UUID = bluetooth.UUID(0x180D)
_HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY, )
_HR_SERVICE = (_HR_UUID, (_HR_CHAR, ), )

# support 'Nordic UART'
_UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
_UART_TX =  (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY, )
_UART_RX =  (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE, )
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX, ), )
_SERVICES = (_HR_SERVICE, _UART_SERVICE, )

def GetAdvPayload(aName: str = None, aServices: list = None, aAppearance: int = 0, aLimitedDisc: bool = False, aBrEdr: bool = False) -> bytearray:
    _ADV_FLAGS = const(0x01)
    _ADV_NAME = const(0x09)
    _ADV_APPEARANCE = const(0x19)
    _ADV_UUID16_COMPLETE = const(0x3)
    _ADV_UUID32_COMPLETE = const(0x5)
    _ADV_UUID128_COMPLETE = const(0x7)

    def _append(aType: int, aValue):
        nonlocal Res
        #print('adv_append', aType, aValue)
        Res += struct.pack("BB", len(aValue) + 1, aType) + aValue

    Res = bytearray()

    Data = struct.pack("B", (0x01 if aLimitedDisc else 0x02) + (0x18 if aBrEdr else 0x04))
    _append(_ADV_FLAGS, Data)

    if (aName):
        _append(_ADV_NAME, bytes(aName, 'UTF-8'))

    if (aServices):
        for Service in aServices:
            Data = bytes(Service)
            if (len(Data) == 2):
                _append(_ADV_UUID16_COMPLETE, Data)
            elif (len(Data) == 4):
                _append(_ADV_UUID32_COMPLETE, Data)
            elif (len(Data) == 16):
                _append(_ADV_UUID128_COMPLETE, Data)

    if (aAppearance):
        _append(_ADV_APPEARANCE, struct.pack("<h", aAppearance))

    return Res

def PrettifyMac(aMac: memoryview) -> str:
    #Str = hexlify(aMac).decode('utf-8')
    return "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB", aMac)

class TBLE:
    def __init__(self, aPayload: bytes):
        self._conns = set()
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._IRQ)
        ( (self._hr, ), (self._tx, self._rx, ), ) = self._ble.gatts_register_services(_SERVICES)

        self._payload = aPayload
        self._Advertise()

    def _Advertise(self, aInterval: int = 500000):
        #self._ble.config(addr_mode=2)
        if (aInterval == 0):
            self._ble.gap_advertise(None)
        else:
            self._ble.gap_advertise(aInterval, adv_data=self._payload)

    def _IRQ(self, aEvent: int, aData):
        if (aEvent == _IRQ_CENTRAL_CONNECT):
            conn_h, _, addr = aData
            self._conns.add(conn_h)
            Log.Print(1, 'i', 'Connect', PrettifyMac(addr))
            self._DoConnect(True, addr)

        elif (aEvent == _IRQ_CENTRAL_DISCONNECT):
            conn_h, _, addr = aData
            if (conn_h in self._conns):
                self._conns.remove(conn_h)
                Log.Print(1, 'i', 'Disconnect', PrettifyMac(addr))
                self._Advertise()
                self._DoConnect(False, addr)

        elif (aEvent == _IRQ_GATTS_WRITE):
            Buf = self._ble.gatts_read(self._rx)
            Msg = Buf.decode('UTF-8').strip()
            self._DoReceive(Msg)

    def _DoReceive(self, aData: str):
        pass

    def _DoConnect(self, aData: str):
        pass

    def Send(self, aData):
        for conn in self._conns:
            self._ble.gatts_notify(conn, self._tx, aData)

    def Close(self):
        for conn_h in self._conns:
            self._ble.gap_disconnect(conn_h)
        self._conns.clear()
