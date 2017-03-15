"""
FMC API Rest Objects

"""
from .object_mixins import _FmcApiObject, NameField, NameWithSpaceField, ModeField, DefaultActionField, ActionField, UuidField, DescriptionField

class SecurityZone(ModeField, NameField, UuidField, DescriptionField, _FmcApiObject):
    """
    Need: name, mode
    Optional: desc
    """
    _type = 'SecurityZone'
    url = 'object/securityzones'

    def valid_for_post(self):
        if self.name and self.mode:
            return True

    """
        json_data = {
            "type": "SecurityZone",
            "name": zone['name'],
            "description": zone['desc'],
            "interfaceMode": zone['mode'],
        }
    """
    def __str__(self):
        property_names = [
            p for p in dir(__class__)
                if isinstance(getattr(__class__, p), property)
            ]
        return_values = {}
        for thing in property_names:
            return_values.update({thing:getattr(self,thing)})
        return "%s" % return_values

class NetworkObject(ModeField, NameField, UuidField, _FmcApiObject):
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


class UrlObject(NameWithSpaceField, UuidField, _FmcApiObject):
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


class AccessControlPolicy(NameWithSpaceField, UuidField, DefaultActionField, _FmcApiObject):
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


class AccessControlPolicyRule(NameWithSpaceField, UuidField, _FmcApiObject):
    """
    Needs: name, action, acpname
    Optional: enabled, sendeventstofmc, logbegin, logend, ipspolicy, sourcezone, destzone, sourcenetwork, destnetwork, and many more!!!
    """
# Create ActionField Mixin in objects for this
# Available Actions: ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    type = 'AccessRule'


class Device(NameWithSpaceField, UuidField, _FmcApiObject):
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

from fmc_wrapper import FMC
from fmc_wrapper.objects import SecurityZone

stuff_to_post = [
    SecurityZone(name="asdf", mode="ROUTED"),
    NetworkObject(name=" asdf1", mode="ROUTED"),
    UrlObject(name="Cisco", value='www.cisco.com')
]

with FMC(host='1.3.4.5',username='admin',password='pass') as fmc1:
  fmc1.post(stuff_to_post)

-----------------------------------------
"""
