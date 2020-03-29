import time
import bluetooth


def OnIrq(event, data):
    print('irq', event, data)


ble = bluetooth.BLE()
ble.active(True)
ble.irq(handler = OnIrq)
ble.gap_advertise(100, adv_data='MicroPython1')

while True:
    print('x')
    time.sleep(1)

