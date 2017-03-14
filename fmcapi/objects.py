"""
FMC API Rest Objects

"""
from .object_mixins import NameField, NameWithSpaceField, ModeField, DefaultAction, UuidField

class SecurityZone(ModeField, NameField, UuidField):
    """
    Need: name, mode
    Optional: desc
    """
    version = 1
    url = '/object/securityzones'
    type = 'SecurityZone'
    name = kwargs['name']
    mode = kwargs['mode']
    if not kwargs['desc']:
        description = 'Created by API'
    else:
        description = kwargs['desc']

    """
        json_data = {
            "type": "SecurityZone",
            "name": zone['name'],
            "description": zone['desc'],
            "interfaceMode": zone['mode'],
        }
    """


class NetworkObject(ModeField, NameField, UuidField):
    """
    Need: name, value
    Optional: desc
    """
    version = 1
    url = '/object/networks'
    type = 'Network'
    name = kwargs['name']
    value = kwargs['value']
    if not kwargs['desc']:
        description = 'Created by API'
    else:
        description = kwargs['desc']

    """
        json_data = {
            'name': obj['name'],
            'value': obj['value'],
            'description': obj['desc'],
            'type': 'Network',
        }
    """


class UrlObject(NameWithSpaceField, UuidField):
    """
    Need: name, value (AKA URL)
    Optional: desc
    """
    version = 1
    url = '/object/urls'
    type = 'Url'
    name = kwargs['name']
    value = kwargs['value']
    if not kwargs['desc']:
        description = 'Created by API'
    else:
        description = kwargs['desc']

    """
            json_data = {
                'name': obj['name'],
                'url': obj['value'],
                'description': obj['desc'],
                'type': 'Url',
            }
    """


class AccessControlPolicy(NameField, UuidField, DefaultAction):
    """
    Needs: name, defaultaction
    Optional: desc
    """
    version = 1
    url = '/policy/accesspolicies'
    type = 'AccessPolicy'
    name = kwargs['name']
    if not kwargs['defaultaction']:
        description = 'BLOCK'
    else:
        description = kwargs['defaultaction']
    if not kwargs['desc']:
        description = 'Created by API'
    else:
        description = kwargs['desc']

    """
        json_data = {
            'type': "AccessPolicy",
            'name': policy['name'],
            'description': policy['desc'],
            'defaultaction': { 'action': policy['defaultaction'] }
        }
    """


class AcpRule(NameField, UuidField):
    """
    Needs: name, action, acpname
    Optional: enabled, sendeventstofmc, logbegin, logend, ipspolicy, sourcezone, destzone, sourcenetwork, destnetwork, and many more!!!
    """
# Available Actions: ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    type = 'AccessRule'
    enabled = True
    pass


class Device(NameWithSpaceField, UuidField):
    """
    Needs: name, regkey, acpname
    Optional: license_caps, hostname
    """
# LICENSE_CAPS = ['MALWARE', 'URLFilter', 'PROTECT', 'CONTROL', 'VPN']
    type = 'Device'
    url = '/devices/devicerecords'
    pass

"""
-----------------------------------------

from fmcapi import FMC
from fmcapi.objects import SecurityZone

stuff_to_post = [
    SecurityZone(name="asdf", mode="ROUTED"),
    NetworkObject(name=" asdf1", mode="ROUTED"),
    UrlObject(name="Cisco", value='www.cisco.com')
]

with FMC(host='1.3.4.5',username='admin',password='pass') as fmc1:
  fmc1.post(stuff_to_post)

-----------------------------------------
"""
