def Main(aConf) -> tuple:
    import bluetooth
    from micropython import const

    from IncP.BLE import GetAdvPayload
    from .Main import TBleEx
    from App import ConfApp

    # org.bluetooth.service.environmental_sensing
    _ENV_SENSE_UUID = bluetooth.UUID(0x181A)
    # org.bluetooth.characteristic.gap.appearance.xml
    _ADV_APPEARANCE_GENERIC_THERMOMETER = const(0x300)

    Payload = GetAdvPayload(aName = ConfApp.get('BLE_Name', 'MyBLE'), aServices = [_ENV_SENSE_UUID], aAppearance = _ADV_APPEARANCE_GENERIC_THERMOMETER)
    Obj = TBleEx(Payload)
    return (Obj, Obj.Run())
