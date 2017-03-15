"""
Object mixins define reused validation logic used by the FMC objects in objects.py

The point of a mixin is to create a type that can be "mixed in" to any other type via inheritance without affecting the inheriting type while still offering some beneficial functionality for that type.


"""

import re


class _FmcApiObject(object):

    def __str__(self):
        # Print/Output JSON String
        pass

class UuidField(object):
    UUIDs = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    _uuid = None

    def __init__(self, *args, **kwargs):
        if 'uuid' in  kwargs:
            self._uuid = kwargs['uuid']

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if not re.match(self.UUIDs, uuid):
            raise Exception("UUID Invalid: %s" % uuid)
        self._uuid = uuid


class DescriptionField(object):
    _description = "Created by API."

    def __init__(self, *args, **kwargs):
        if 'decription' in kwargs:
            self.description = kwargs['description']

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


class NameField(object):
    NAME_VALUES = "^[\w\d][.\w\d_\-]*$"

    _name = None

    def __init__(self, *args, **kwargs):
         if 'name' in kwargs:
             self.name = kwargs['name']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not re.match(self.NAME_VALUES, name):
            raise Exception("Only alpha-numeric, underscrore and hyphen characters are permitted: %s" % name)
        self._name = name

class ModeField(object):

    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    _mode = None

    def __init__(self, *args, **kwargs):
         if 'mode' in kwargs:
             self.name = kwargs['mode']

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (self._mode, ", ".join(self.MODE_CHOICES)))
        self._mode = mode

class DefaultAction(object):
    """
    Needs work
    """
    ACTION_CHOICES = ['BLOCK', 'PERMIT', 'TRUST', 'MONITOR', 'BLOCK_WITH_RESET', 'INTERACTIVE_BLOCK', 'INTERACTIVE_BLOCK_WITH_RESET', 'NETWORK_DISCOVERY', 'IPS_ACTION', 'FASTPATH']

    _defaultaction = None

    def __init__(self, *args, **kwargs):
         if 'defaultaction' in kwargs:
             self.name = kwargs['defaultaction']

    @property
    def mode(self):
        return self._defaultaction

    @mode.setter
    def mode(self, defaultaction):
        if defaultaction not in self.ACTION_CHOICES:
            raise Exception('User provided defaultaction: "%s" is valid: "%s".' % (self._defaultaction, ", ".join(self.ACTION_CHOICES)))
        self._defaultaction = defaultaction


class NameWithSpaceField(object):
    NAME_VALUES = "^[\w\d][.\w\d_\- ]*$"

    _name = None

    def __init__(self, *args, **kwargs):
         if 'name' in kwargs:
             self.name = kwargs['name']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not re.match(self.NAME_VALUES, name):
            raise Exception("Only alpha-numeric, underscrore, hyphen, and space characters are permitted: %s" % name)
        self._name = name
