import re
import fmc_wrapper.API


class _NameRequired(object):
    """
    Check to see wheather keyword 'name' contains only:
    Alpha, numeric, underscore, and hyphen only.  (Starts with alpha or numeric too.)
    """
    NAME_VALUES = "^[\w\d][\w\d_-]*$"

    def __init__(self, *args, **kwargs):
        if not re.match(self.NAME_VALUES, kwargs['name']):
            raise Exception("Only Alpha-numeric, Underscore, and Hyphen characters are permitted: %s" % kwargs['name'])


class _ModeValidate(object):
    """
    Ensure that keyword value 'mode' is a proper value.
    """
    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    def __init__(self, *args, **kwargs):
        if kwargs['mode'] not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (kwargs['mode'], ", ".join(self.MODE_CHOICES)))


class Post(_NameRequired, _ModeValidate, object):
    """
    Creates a JSON formatted variable and POSTs it to the FMC.

    Currently only accepts name, mode, and desc variables.
    """

    def __init__(self, *args, **kwargs):
        self.REQUIRED_PARAMS = ['name', 'mode']
        for param in self.REQUIRED_PARAMS:
            if param not in kwargs.keys():
                raise Exception("%s is required." % param)
        super().__init__(*args, **kwargs)
        _NameRequired(**kwargs)
        _ModeValidate(**kwargs)
        self.name = kwargs['name']
        self.mode = kwargs['mode']
        self.type = 'SecurityZone'
        self.url = '/object/securityzones'
        if 'desc' in kwargs:
            self.desc = kwargs['desc']
        else:
            self.desc = "Security Zone created by API."

        json_data = {
            "type": self.type,
            "name": self.name,
            "description": self.desc,
            "interfaceMode": self.mode,
        }

        print("Creating Security Zones.")
        print(json_data)
        response = fmc_wrapper.API.PostData(self, self.url, json_data)
#        if 'id' not in response:
#            raise Exception("Creation of Security Zone failed.")
#        self.id = response['id']
        print("\tSecurity Zone %s created." % self.name)
