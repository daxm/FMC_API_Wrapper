"""
Object mixins define reused validation logic used by the FMC objects in objects.py

The point of a mixin is to create a type that can be "mixed in" to any other type via inheritance without affecting the inheriting type while still offering some beneficial functionality for that type.


"""

import types
import re
import json


class _FmcApiObject(types.SimpleNamespace):
    """
    Methods for dealing with misc items used by other object_mixins and/or objects.
    """

    _type = None

    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
               print("Unknown attribute %s=%s" % (k,v))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
 
    def __str__(self):
        property_names = [
            p for p in dir(self.__class__)
                if isinstance(getattr(self.__class__, p), property)
            ]
        prop_dict = {}
        for prop in property_names:
            val = getattr(self, prop)
            if val:
                prop_dict[prop] = val
        return json.dumps(prop_dict)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class UuidField(object):
    """
    Used as a keyword checker for the field "id".
    """

    _VALID_UUID = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    _uuid = None

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if not re.match(self._VALID_UUID, uuid):
            raise Exception("UUID Invalid: %s" % uuid)
        self._uuid = uuid


class DescriptionField(object):
    """
    Used in many of the Objects and Policies.  References the keyword "description".
    """

    _description = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


class ValueField(object):
    """
    "value" is used as the keyword for the Network Object.
    Not sure whether it is used somewhere else for some othe purpose.
    """

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class UrlField(object):
    """
    "url" is used as the keyword for the URL Object.
    """

    _url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


class NameField(object):
    """
    "name" is used throughout many Objects and Policies.
    """

    _VALID_NAME = "^[\w\d][.\w\d_\-]*$"
    _ERROR_MESSAGE = "Only alpha-numeric, underscore and hyphen characters are permitted: %s"

    _name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not re.match(self._VALID_NAME, name):
            raise Exception(self._ERROR_MESSAGE % name)
        self._name = name


class NameWithSpaceField(NameField):
    """
    "name" field but allow spaces in name.
    """ 

    _VALID_NAME = "^[\w\d][.\w\d_\- ]*$"
    _ERROR_MSG = "Only alpha-numeric, underscore, hyphen, and space characters are permitted"


class HostnameField(object):
    """
    "hostName" is used throughout many Objects and Policies.
    """

    _VALID_HOSTNAME = "^[\w\d][.\w\d_\- ]*$"
    _ERROR_MESSAGE = "Only alpha-numeric, underscore, hyphen and space characters are permitted: %s"

    _hostname = None

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        if not re.match(self._VALID_HOSTNAME, hostname):
            raise Exception(self._ERROR_MESSAGE % hostname)
        self._hostname = hostname


class ModeField(object):
    """
    "mode" is used as the keyword for the mode of the FTD.  (Routed, Transparent, etc.)
    """

    _MODE_CHOICES = ['ROUTED', 'TRANSPARENT']
    _mode = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in self._MODE_CHOICES:
            raise Exception('Mode must be one of the following: "%s".' % (", ".join(self._MODE_CHOICES)))
        self._mode = mode


class InterfaceModeField(object):
    """
    "interfaceMode"
    """

    _INTERFACE_MODE_CHOICES = ['PASSIVE', 'INLINE', 'SWITCHED', 'ROUTED', 'ASA']
    _interfaceMode = None

    @property
    def interfaceMode(self):
        return self._mode

    @interfaceMode.setter
    def interfaceMode(self, interfaceMode):
        if interfaceMode not in self._INTERFACE_MODE_CHOICES:
            raise Exception('interfaceMode: %s must be one of the following: "%s".' % (interfaceMode, ", ".join(self._INTERFACE_MODE_CHOICES)))
        self._interfaceMode = interfaceMode


class DefaultActionField(object):
    """
    "defaultaction" is used as the keyword in specifying the Default Action of an Access Control Policy.
    """

    _DEFAULT_ACTION_CHOICES = ['BLOCK', 'PERMIT', 'TRUST', 'MONITOR', 'BLOCK_WITH_RESET', 'INTERACTIVE_BLOCK', 'INTERACTIVE_BLOCK_WITH_RESET', 'NETWORK_DISCOVERY', 'IPS_ACTION', 'FASTPATH']

    _defaultaction = None

    @property
    def defaultAction(self):
        return self._defaultaction

    @defaultAction.setter
    def defaultAction(self, defaultaction):
        if defaultaction not in self._DEFAULT_ACTION_CHOICES:
            raise Exception('User provided defaultaction: "%s" is invalid: must be one of: "%s".' % (defaultaction, ", ".join(self._DEFAULT_ACTION_CHOICES)))
        self._defaultaction = defaultaction


class ActionField(object):
    """
    "action" is used as the keyword in Access Control Policy Rules.
    """
    ACTION_CHOICES = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    _action = None

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if action not in self.ACTION_CHOICES:
            raise Exception('Action: "%s" must be one of: "%s".' % (self._action, ", ".join(self.ACTION_CHOICES)))
        self._action = action


class AcpNameToUuid(object):
    """
    Take an ACP name and return its UUID.
    """
    _acpuuid = None

    @property
    def acpuuid(self):
        return self._acpuuid

    @acpuuid.setter
    def acpuuid(self, acpuuid):
        """
        Query FMC with ACP Name and get it's UUID.
        """
        self._acpuuid = acpuuid


class NetworkObjectNameToUuid(object):
    """
    Take an Network Object 'name' and return its UUID.
    This would be used in the sourceNetwork, destNetworks in ACPRule.
    We will need something like this too for the UrlName.
    """
    pass


class RegkeyField(object):
    """
    "regkey" used as keyword for the Registration Key when POSTing Devices.
    """
    _regkey = None

    @property
    def regkey(self):
        return self._regkey

    @regkey.setter
    def regkey(self, regkey):
        self._regkey = regkey


class NatIdField(object):
    """
    "natId" used as keyword for the NAT ID when POSTing Devices.
    """
    _natId = None

    @property
    def natId(self):
        return self._natId

    @natId.setter
    def natId(self, natId):
        self._natId = natId


class SourceNetworkField(object):
    """
    """
    _sourceNetwork = None

    @property
    def sourceNetwork(self):
        return self._sourceNetwork

    @sourceNetwork.setter
    def sourceNetwork(self, sourceNetwork):
        self._sourceNetwork = sourceNetwork


class DestNetworkField(object):
    """
    """
    _destNetwork = None

    @property
    def destNetwork(self):
        return self._destNetwork

    @destNetwork.setter
    def destNetwork(self, destNetwork):
        self._destNetwork = destNetwork

