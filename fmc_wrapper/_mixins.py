import re


class _ValueSyntax1(object):
    """
    Check to see wheather user provided value for this keyword contains only:
    Alpha, numeric, underscore, and hyphen only.  (Starts with alpha or numeric too.)
    """
    NAME_VALUES = "^[\w\d][\w\d_-]*$"

    def __init__(self, **kwargs):

        if not re.match(self.NAME_VALUES, key):
            raise Exception("Only Alpha-numeric, Underscore, and Hyphen characters are permitted: %s" % key)


class _ValueSyntax2(object):
    """
    Check to see wheather user provided value for this keyword contains only:
    Alpha, numeric, underscore, hyphen, and whitespace only.  (Starts with alpha or numeric too.)
    """
    NAME_VALUES = "^[\w\d][\w\d\s_-]*$"

    def __init__(self, *args, **kwargs):
        if not re.match(self.NAME_VALUES, kwargs['name']):
            raise Exception("Only Alpha-numeric, Underscore, Hyphen, and Space characters are permitted: %s" % kwargs['name'])


class _SecurityZoneModeOptions(object):
    """
    Ensure that keyword value 'mode' is a proper value.
    """
    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    def __init__(self, *args, **kwargs):
        if kwargs['mode'] not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (kwargs['mode'], ", ".join(self.MODE_CHOICES)))

class _RequiredParams(object):
    """
    Check the list of required keywords against the user provided keywords.
    """
    def __init__(self, **kwargs):
        for param in self.REQUIRED_PARAMS:
            if param not in kwargs.keys():
                raise Exception("%s is required." % param)
