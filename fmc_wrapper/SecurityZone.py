import re


class _NameRequired(object):
    NAME_VALUES = "^[\w\d][\w\d_-]*$"
    REQUIRED_PARAMS = ['name']

    def __init__(self, *args, **kwargs):
        for param in self.REQUIRED_PARAMS:
            if param not in kwargs:
                raise Exception("%s is required." % param)
        if re.match(self.NAME_VALUES, kwargs['name']):
            raise Exception("Whitespace not permitted in name.")
        super().__init__()


class _ModeRequired(object):
    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    def __init__(self, *args, **kwargs):
        if kwargs['mode'] not in self.MODE_CHOICES:
            raise Exception("User provided mode: %s is not a valid mode: %s." % (kwargs['mode'], ",".join(kwargs['mode'])))
        super().__init__()


class SecurityZone(_NameRequired, _ModeRequired, object):
    def __init__(self, *args, **kwargs):
        super().__init__()
