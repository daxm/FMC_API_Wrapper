"""
Object mixins define reused validation logic used by the FMC objects in objects.py

The point of a mixin is to create a type that can be "mixed in" to any other type via inheritance without affecting the inheriting type while still offering some beneficial functionality for that type.


"""

import re
import json


class _FmcApiObject(object):
    """
    Methods for dealing with misc items used by other object_mixins and/or objects.
    """

    _type = None
    _type_field = 'type'

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
 
    def __init__(self, *args, **kwargs):
        if self._type_field in kwargs:
            self.type = kwargs[self._type_field]

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

    UUIDs = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    _uuid = None
    _uuid_field = 'id'

    def __init__(self, *args, **kwargs):
        if self._uuid_field in kwargs:
            self.uuid = kwargs[self._uuid_field]
        super().__init__(self, *args, **kwargs)

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if not re.match(self.UUIDs, uuid):
            raise Exception("UUID Invalid: %s" % uuid)
        self._uuid = uuid


class DescriptionField(object):
    """
    Used in many of the Objects and Policies.  References the keyword "description".
    """

    _description = None
    _description_field = 'description'

    def __init__(self, *args, **kwargs):
        if self._description_field in kwargs:
            self.description = kwargs[self._description_field]
        super().__init__(self, *args, **kwargs)


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
    _value_field = 'value'

    def __init__(self, *args, **kwargs):
        if self._value_field in kwargs:
            self.value = kwargs[self._value_field]
        super().__init__(self, *args, **kwargs)


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
    _url_field = 'url'

    def __init__(self, *args, **kwargs):
        if self._url_field in kwargs:
            self.url = kwargs[self._url_field]
        super().__init__(self, *args, **kwargs)


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

    NAME_VALUES = "^[\w\d][.\w\d_\-]*$"
    ERROR_MESSAGE = "Only alpha-numeric, underscore and hyphen characters are permitted: %s"

    _name = None
    _name_field = 'name'

    def __init__(self, *args, **kwargs):
        if self._name_field in kwargs:
            self.name = kwargs[self._name_field]
        super().__init__(self, *args, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not re.match(self.NAME_VALUES, name):
            raise Exception(self.ERROR_MESSAGE % name)
        self._name = name


class NameWithSpaceField(NameField):
    """
    "name" field but allow spaces in name.
    """ 

    NAME_VALUES = "^[\w\d][.\w\d_\- ]*$"
    ERROR_MSG = "Only alpha-numeric, underscore, hyphen, and space characters are permitted"


class HostnameField(object):
    """
    "hostName" is used throughout many Objects and Policies.
    """

    HOSTNAME_VALUES = "^[\w\d][.\w\d_\- ]*$"
    ERROR_MESSAGE = "Only alpha-numeric, underscore, hyphen and space characters are permitted: %s"

    _hostname = None
    _hostname_field = 'hostname'

    def __init__(self, *args, **kwargs):
        if self._hostname_field in kwargs:
            self.hostname = kwargs[self._hostname_field]
        super().__init__(self, *args, **kwargs)

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        if not re.match(self.HOSTNAME_VALUES, hostname):
            raise Exception(self.ERROR_MESSAGE % hostname)
        self._hostname = hostname


class ModeField(object):
    """
    "mode" is used as the keyword for the mode of the FTD.  (Routed, Transparent, etc.)
    """

    _MODE_CHOICES = ['ROUTED', 'TRANSPARENT']
    _mode = None
    _mode_field = 'mode'

    def __init__(self, *args, **kwargs):
        if self._mode_field in kwargs:
            self.mode = kwargs[self._mode_field]
        super().__init__(self, *args, **kwargs)

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
    _interfaceMode_field = 'interfaceMode'

    def __init__(self, *args, **kwargs):
        if self._interfaceMode_field in kwargs:
            self.interfaceMode = kwargs[self._interfaceMode_field]
        super().__init__(self, *args, **kwargs)

    @property
    def interfaceMode(self):
        return self._mode

    @interfaceMode.setter
    def interfaceMode(self, interfaceMode):
        if interfaceMode not in self._INTERFACE_MODE_CHOICES:
            raise Exception('interfaceMode must be one of the following: "%s".' % (", ".join(self._INTERFACE_MODE_CHOICES)))
        self._interfaceMode = interfaceMode



class DefaultActionField(object):
    """
    "defaultaction" is used as the keyword in specifying the Default Action of an Access Control Policy.
    """

    DEFAULT_ACTION_CHOICES = ['BLOCK', 'PERMIT', 'TRUST', 'MONITOR', 'BLOCK_WITH_RESET', 'INTERACTIVE_BLOCK', 'INTERACTIVE_BLOCK_WITH_RESET', 'NETWORK_DISCOVERY', 'IPS_ACTION', 'FASTPATH']

    _defaultaction = None
    _defaultaction_field = 'defaultAction'

    def __init__(self, *args, **kwargs):
        if self._defaultaction_field in kwargs:
            self.defaultaction = kwargs[self._defaultaction_field]
        super().__init__(self, *args, **kwargs)

    @property
    def defaultaction(self):
        return self._defaultaction

    @defaultaction.setter
    def defaultaction(self, defaultaction):
        if defaultaction not in self.DEFAULT_ACTION_CHOICES:
            raise Exception('User provided defaultaction: "%s" is valid: "%s".' % (self._defaultaction, ", ".join(self.DEFAULT_ACTION_CHOICES)))
        self._defaultaction = defaultaction


class ActionField(object):
    """
    "action" is used as the keyword in Access Control Policy Rules.
    """
    ACTION_CHOICES = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    _action = None
    _action_field = 'action'

    def __init__(self, *args, **kwargs):
        if self._action_field in kwargs:
            self.action = kwargs[self._action_field]
        super().__init__(self, *args, **kwargs)

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
    _acpuuid_field = 'acpName'

    def __init__(self, *args, **kwargs):
        if self._acpuuid_field in kwargs:
            self.acpuuid = kwargs[self._acpuuid_field]
        super().__init__(self, *args, **kwargs)

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
    _regkey_field = 'regkey'

    def __init__(self, *args, **kwargs):
        if self._regkey_field in kwargs:
            self.regkey = kwargs[self._regkey_field]
        super().__init__(self, *args, **kwargs)

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
    _natId_field = 'natId'

    def __init__(self, *args, **kwargs):
        if self._natId_field in kwargs:
            self.natId = kwargs[self._natId_field]
        super().__init__(self, *args, **kwargs)

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
    _sourceNetwork_field = 'sourceNetwork'

    def __init__(self, *args, **kwargs):
        if self._sourceNetwork_field in kwargs:
            self.sourceNetwork = kwargs[self._sourceNetwork_field]
        super().__init__(self, *args, **kwargs)

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
    _destNetwork_field = 'destNetwork'

    def __init__(self, *args, **kwargs):
        if self._destNetwork_field in kwargs:
            self.destNetwork = kwargs[self._destNetwork_field]
        super().__init__(self, *args, **kwargs)

    @property
    def destNetwork(self):
        return self._destNetwork

    @destNetwork.setter
    def destNetwork(self, destNetwork):
        self._destNetwork = destNetwork

