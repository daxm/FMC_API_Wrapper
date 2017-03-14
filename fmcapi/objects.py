"""
FMC API Rest Objects

"""
from .object_mixins import _AbstractField, NameField, NameWithSpaceField, ModeField, DefaultAction, UuidField

class SecurityZone(ModeField, NameField, UuidField, _AbstractField):
    """
    Need: name, mode
    Optional: desc
    """
    _type = 'SecurityZone'
    url = 'object/securityzones'

    """
        json_data = {
            "type": "SecurityZone",
            "name": zone['name'],
            "description": zone['desc'],
            "interfaceMode": zone['mode'],
        }
    """


class Network(ModeField, NameField, UuidField, _AbstractField):
    """
    Need: name, value
    Optional: desc
    """
    _type = 'Network'
    url = 'object/networks'
    

    """
        json_data = {
            'name': obj['name'],
            'value': obj['value'],
            'description': obj['desc'],
            'type': 'Network',
        }
    """


class Url(NameWithSpaceField, UuidField, _AbstractField):
    """
    Need: name, value (AKA URL)
    Optional: desc
    """
    _type = 'Url'
    url = 'object/urls'
    

    """
            json_data = {
                'name': obj['name'],
                'url': obj['value'],
                'description': obj['desc'],
                'type': 'Url',
            }
    """


class AccessPolicy(NameField, UuidField, DefaultAction, _AbstractField):
    """
    Needs: name, defaultaction
    Optional: desc
    """
    _type = 'AccessPolicy'
    url = 'policy/accesspolicies'

    """
        json_data = {
            'type': "AccessPolicy",
            'name': policy['name'],
            'description': policy['desc'],
            'defaultaction': { 'action': policy['defaultaction'] }
        }
    """


class AccessRule(NameField, UuidField, _AbstractField):
    """
    Needs: name, action, acpname
    Optional: enabled, sendeventstofmc, logbegin, logend, ipspolicy, sourcezone, destzone, sourcenetwork, destnetwork, and many more!!!
    """
# Create ActionField Mixin in objects for this
# Available Actions: ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    type = 'AccessRule'


class Device(NameWithSpaceField, UuidField, _AbstractField):
    """
    Needs: name, regkey, acpname
    Optional: license_caps, hostname
    """
# Create LicenseCapsField Mixin in objects for this
# LICENSE_CAPS = ['MALWARE', 'URLFilter', 'PROTECT', 'CONTROL', 'VPN']
    type = 'Device'
    url = 'devices/devicerecords'

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
