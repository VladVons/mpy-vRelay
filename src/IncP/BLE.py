'''
Author:      Vladimir Vons, Oster Inc
Created:     2022.01.11
License:     GNU, see LICENSE for more details
Description:

https://mpython.readthedocs.io/en/master/library/micropython/ubluetooth.html
'''

import bluetooth
from micropython import const
import struct


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX =  (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY, )
_UART_RX =  (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE, )
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX), )

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(0x300)


def GetAdvPayload(aLimitedDisc=False, aBrEdr=False, aName=None, aServices=None, aAppearance=0):
    _ADV_FLAGS = const(0x01)
    _ADV_NAME = const(0x09)
    _ADV_APPEARANCE = const(0x19)
    _ADV_UUID16_COMPLETE = const(0x3)
    _ADV_UUID32_COMPLETE = const(0x5)
    _ADV_UUID128_COMPLETE = const(0x7)

    def _append(aType, aValue):
        nonlocal Res
        print('adv_append', aType, aValue)
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


class TBLE:
    def __init__(self, aName):
        self._conns = set()
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx, self._rx),) = self._ble.gatts_register_services((_UART_SERVICE, ))

        self._payload = GetAdvPayload(aName=aName, aServices=[_ENV_SENSE_UUID], aAppearance=_ADV_APPEARANCE_GENERIC_THERMOMETER)
        self._advertise()

    def _advertise(self, aInterval=500000):
        self._ble.gap_advertise(aInterval, adv_data=self._payload)

    def _irq(self, aEvent, aData):
        if (aEvent == _IRQ_CENTRAL_CONNECT):
            conn_h, addr_type, addr = aData
            print('---x EvConn', conn_h, addr_type, addr)
            self._conns.add(conn_h)
            self._advertise()
        elif (aEvent == _IRQ_CENTRAL_DISCONNECT):
            conn_h, addr_type, addr = aData
            print('---x EvDConn', conn_h, addr_type, addr)
            if (conn_h in self._conns):
                self._conns.remove(conn_h)
            self._advertise()
        elif (aEvent == _IRQ_GATTS_WRITE):
            conn_h, attr_h = aData
            print('---x EvWrite', conn_h, attr_h)
            Buf = self._ble.gatts_read(self._rx)
            Msg = Buf.decode('UTF-8').strip()
            print('---x EvWrite Msg', Msg)
        else:
            print('---x EvElse', aEvent, aData)


    def Write(self, aData):
        print('---x write', aData)
        for conn in self._conns:
            print('---x write dev', conn, aData)
            self._ble.gatts_notify(conn, self._tx, aData)

    def Close(self):
        for conn_h in self._conns:
            self._ble.gap_disconnect(conn_h)
        self._conns.clear()
