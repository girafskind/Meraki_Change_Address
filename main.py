"""
This Python script will change the address for all Meraki devices in a given organization
"""


import meraki
import config

dashboard = meraki.DashboardAPI(config.API_KEY, suppress_logging=True)


def get_devices_in_network(net_id):
    """
    Returns list of serials found within that network.
    :param net_id: Network ID.
    :return: List of serials.
    """
    devices_in_network = dashboard.networks.getNetworkDevices(net_id)

    devices = []

    for device in devices_in_network:
        devices.append(device['serial'])

    return devices


def get_device_address(serial):
    """
    Function for retrieving the address of a given serial.
    :param serial: Device serial.
    :return: Address of device.
    """
    address = dashboard.devices.getDevice(serial)['address']

    return address


def set_device_address(serial, overwrite=False):
    """
    Sets the address of given device, address is given in config.py file.
    :param serial: Serial number of the device.
    :param overwrite: If set, it will overwrite even if the device already has an address.
    :return: Nothing.
    """
    current_address = get_device_address(serial)
    if len(current_address) == 0 or overwrite:
        dashboard.devices.updateDevice(serial, address=config.DEVICE_ADDRESS)
    else:
        print("Device already has an address: \n" + current_address)
        print("Do you want to overwrite it with \n" + config.DEVICE_ADDRESS + "?")

        while overwrite != ("y" or "n"):
            overwrite = input("(y/n)")
            if overwrite == "y":
                dashboard.devices.updateDevice(serial, address=config.DEVICE_ADDRESS)
                break
            elif overwrite == "n":
                break
            else:
                print("Answer must be \"y\" or \"n\"")


def main():
    """
    Main program file
    :return:
    """
    devices_in_network = get_devices_in_network(config.NET_ID)

    for device in devices_in_network:
        set_device_address(device, overwrite=False)


if __name__ == '__main__':
    main()
