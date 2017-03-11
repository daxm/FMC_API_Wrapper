import re
import fmc_wrapper.FMC


class _NameRequired(object):
    # Alpha, numeric, underscore, and hyphen only.  (Starts with alpha or numeric too.)
    NAME_VALUES = "^[\w\d][\w\d_-]*$"

    def __init__(self, *args, **kwargs):
        if not re.match(self.NAME_VALUES, kwargs['name']):
            raise Exception("Only Alpha-numeric, Underscore, and Hyphen characters are permitted: %s" % kwargs['name'])


class _ModeValidate(object):
    MODE_CHOICES = ['ROUTED', 'TRANSPARENT']

    def __init__(self, *args, **kwargs):
        if kwargs['mode'] not in self.MODE_CHOICES:
            raise Exception('User provided mode: "%s" is not a valid mode: "%s".' % (kwargs['mode'], ", ".join(self.MODE_CHOICES)))


class SecurityZone(_NameRequired, _ModeValidate, object):
    """
    Currently only accepts name, mode, and desc variables.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.REQUIRED_PARAMS = ['name', 'mode']
        for param in self.REQUIRED_PARAMS:
            if param not in kwargs.keys():
                raise Exception("%s is required." % param)
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
        fmc1 = fmc_wrapper.FMC()
#        response = fmc1.postdata(self.url, json_data)
#        if 'id' not in response:
#            raise Exception("Creation of Security Zone failed.")
#        self.id = response['id']
        print("\tSecurity Zone %s created." % self.name)

SecurityZone(name='asdf', mode='ROUTED')

