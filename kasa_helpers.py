import asyncio
from kasa import Discover
from kasa.smartdevice import SmartDevice


def get_device_by_alias(alias: str):
    found_devices = asyncio.run(Discover.discover())
    device_values = list(found_devices.values)
    return next((device for device in device_values if device.alias == alias), None)


def turn_device_on(device: SmartDevice):
    asyncio.run(device.update())
    asyncio.run(device.turn_on())


def turn_device_off(device: SmartDevice):
    asyncio.run(device.update())
    asyncio.run(device.turn_off())
