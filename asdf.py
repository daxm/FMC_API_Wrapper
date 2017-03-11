import re


class _NameRequired(object):
    NAME_VALUES = "^[\w\d][\w\d_-]*$"
    REQUIRED_PARAMS = ['name', 'mode']

    def __init__(self, *args, **kwargs):
        print("KWARGS -->", kwargs)
        for param in self.REQUIRED_PARAMS:
            if param not in kwargs.keys():
                raise Exception("%s is required." % param)
        if not re.match(self.NAME_VALUES, kwargs['name']):
            raise Exception("Only Alpha-numeric, Underscore, and Hyphen characters are permitted: %s" % kwargs['name'])
        super().__init__()


class _ModeValidate(object):
    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    def __init__(self, *args, **kwargs):
        if kwargs['mode'] not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (kwargs['mode'], ", ".join(self.MODE_CHOICES)))
        super().__init__()


class SecurityZone(_NameRequired, _ModeValidate, object):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = kwargs['name']
        self.mode = kwargs['mode']

    def __str__(self):
        print(self.name)

sz1 = SecurityZone(name="asdf", mode="ROUTED")

#print(sz1)
