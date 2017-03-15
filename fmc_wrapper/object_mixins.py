"""
Object mixins define reused validation logic used by the FMC objects in objects.py

The point of a mixin is to create a type that can be "mixed in" to any other type via inheritance without affecting the inheriting type while still offering some beneficial functionality for that type.


"""

import re


class _FmcApiObject(object):
    pass

class UuidField(object):
    """
    """

    UUIDs = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    _uuid = None
    _field = 'uuid'

    def __init__(self, *args, **kwargs):
        if(self._field in self._fields):
            raise Exception("%s field added more than once" % field)
        _fields.append(self._field)
        if _field in kwargs:
            self._uuid = kwargs[self._field]

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
    """

    _description = "Created by API."
    _field = 'description'

    def __init__(self, *args, **kwargs):
        if(self._field in self._fields):
            raise Exception("%s field added more than once" % field)
        _fields.append(self._field)
        if _field in kwargs:
            self._description = kwargs[self._field]

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


class NameField(object):
    """
    """

    NAME_VALUES = "^[\w\d][.\w\d_\-]*$"
    ERROR_MESSAGE = "Only alpha-numeric, underscrore and hyphen characters are permitted: %s"

    _name = None
    _field = 'name'

    def __init__(self, *args, **kwargs):
        if(self._field in self._fields):
            raise Exception("%s field added more than once" % field)
        _fields.append(self._field)
        if _field in kwargs:
            self._name = kwargs[self._field]


    def __init__(self, *args, **kwargs):
         if 'name' in kwargs:
             self.name = kwargs['name']

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
    """ 

    NAME_VALUES = "^[\w\d][.\w\d_\- ]*$"
    ERROR_MSG = "Only alpha-numeric, underscrore, hyphen, and space characters are permitted"

class ModeField(object):
    """
    """

    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    _mode = None

    def __init__(self, *args, **kwargs):
         if 'mode' in kwargs:
             self._mode = kwargs['mode']

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (self._mode, ", ".join(self.MODE_CHOICES)))
        self._mode = mode

class DefaultActionField(object):
    """
    Needs work
    """

    DEFAULT_ACTION_CHOICES = ['BLOCK', 'PERMIT', 'TRUST', 'MONITOR', 'BLOCK_WITH_RESET', 'INTERACTIVE_BLOCK', 'INTERACTIVE_BLOCK_WITH_RESET', 'NETWORK_DISCOVERY', 'IPS_ACTION', 'FASTPATH']

    _defaultaction = None

    def __init__(self, *args, **kwargs):
         if 'defaultaction' in kwargs:
             self._defaultaction = kwargs['defaultaction']

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
    """
    ACTION_CHOICES = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    _action = None

    def __init__(self, *args, **kwargs):
         if 'action' in kwargs:
             self._action = kwargs['action']

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if action not in self.ACTION_CHOICES:
            raise Exception('Action: "%s" must be one of: "%s".' % (self._action, ", ".join(self.ACTION_CHOICES)))
        self._action = action



