"""
Object mixins define reused validation logic used by the FMC objects in objects.py

The point of a mixin is to create a type that can be "mixed in" to any other type via inheritance without affecting the inheriting type while still offering some beneficial functionality for that type.


"""

import re
import json


class _FmcApiObject(object):
    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        property_names = [
            p for p in dir(self.__class__)
                if isinstance(getattr(self.__class__, p), property)
            ]
        return_values = {}
        for thing in property_names:
            return_values.update({thing:getattr(self,thing)})
        return json.dumps(return_values)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class UuidField(object):
    """
    """

    UUIDs = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    _uuid = None
    _uuid_field = 'id'

    def __init__(self, *args, **kwargs):
        if self._uuid_field in kwargs:
            self.name = kwargs[self._uuid_field]
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
    """

    _description = "Created by API."
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


class NameField(object):
    """
    """

    NAME_VALUES = "^[\w\d][.\w\d_\-]*$"
    ERROR_MESSAGE = "Only alpha-numeric, underscrore and hyphen characters are permitted: %s"

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
    """ 

    NAME_VALUES = "^[\w\d][.\w\d_\- ]*$"
    ERROR_MSG = "Only alpha-numeric, underscrore, hyphen, and space characters are permitted"


class ModeField(object):
    """
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


class DefaultActionField(object):
    """
    Needs work
    """

    DEFAULT_ACTION_CHOICES = ['BLOCK', 'PERMIT', 'TRUST', 'MONITOR', 'BLOCK_WITH_RESET', 'INTERACTIVE_BLOCK', 'INTERACTIVE_BLOCK_WITH_RESET', 'NETWORK_DISCOVERY', 'IPS_ACTION', 'FASTPATH']

    _defaultaction = None
    _defaultaction_field = 'defaultaction'

    def __init__(self, *args, **kwargs):
        if self._defaultaction_field in kwargs:
            self.name = kwargs[self._defaultaction_field]
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
    """
    ACTION_CHOICES = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE', 'BLOCK_RESET_INTERACTIVE']

    _action = None
    _action_field = 'action'

    def __init__(self, *args, **kwargs):
        if self._action_field in kwargs:
            self.name = kwargs[self._action_field]
        super().__init__(self, *args, **kwargs)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if action not in self.ACTION_CHOICES:
            raise Exception('Action: "%s" must be one of: "%s".' % (self._action, ", ".join(self.ACTION_CHOICES)))
        self._action = action



