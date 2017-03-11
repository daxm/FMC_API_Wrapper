# This script takes a greenfield FMC and sets it up for the FTD v6.2.1 Lab.

import fmcapi

# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '172.16.100.100'
username = 'apiadmin'
password = 'C1sco12345'

# FTD Devices.  Must provide: hostName, acpName, regkey
devices = [
    {
        'name': 'FTD1', 'hostName': '172.16.100.10', 'acpName': 'HQ', 'regkey': 'cisco123', 'version': '6.2.1',
        'licenses': ['BASE', 'THREAT', 'MALWARE', 'URLFilter'],
    },
    {
        'name': 'FTD2', 'hostName': '172.16.100.11', 'acpName': 'HQ', 'regkey': 'cisco123', 'version': '6.2.1',
        'licenses': ['BASE', 'THREAT', 'MALWARE', 'URLFilter'],
    },
]

# FTD Device Attributes.
deviceattributes = [
    {
        'deviceName': 'FTD1',
        'physicalInterfaces':
            [
                {
                    'ipv4': {
                        'static': {
                            'address': '172.16.100.1',
                            'netmask': '24',
                        },
                    },
                    'ifName': 'LAN',
                    'securityZone': 'IN',
                    'name': 'GigabitEthernet0/0',
                },
                {
                    'ipv4': {
                        'static': {
                            'address': '198.18.1.2',
                            'netmask': '24',
                        },
                    },
                    'ifName': 'ISP',
                    'securityZone': 'OUT',
                    'name': 'GigabitEthernet0/1',
                },
            ],
    },
    {
        'deviceName': 'FTD2',
        'physicalInterfaces':
            [
                {
                    'ipv4': {
                        'static': {
                            'address': '172.16.100.2',
                            'netmask': '24',
                        },
                    },
                    'ifName': 'LAN',
                    'securityZone': 'IN',
                    'name': 'GigabitEthernet0/0',
                },
                {
                    'ipv4': {
                        'static': {
                            'address': '198.18.1.3',
                            'netmask': '24',
                        },
                    },
                    'ifName': 'ISP',
                    'securityZone': 'OUT',
                    'name': 'GigabitEthernet0/1',
                },
            ],
    },
]

# ########################################### Main Program ####################################################
with fmcapi.Cluster(serverIP, username=username, password=password) as fmc1:
    # Add FTD devices to FMC
    fmc1.registerdevices(devices)

    # Modify FTD devices
    # DOESN'T WORK YET
    # fmc1.modifydevice_physicalinterfaces(deviceattributes)
