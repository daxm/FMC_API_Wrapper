from . import _mixins
from . import export


@export
class SecurityZone(_NameRequired, _ModeValidate, object):
    """
    Gathers and validates user submitted data in preparation for POST'ing to the FMC.
    Currently only accepts name, mode, and desc variables.
    """

    def __init__(self, *args, **kwargs):
        self.REQUIRED_PARAMS = ['name', 'mode']
        super().__init__(*args, **kwargs)
        self.name = kwargs['name']
        self.mode = kwargs['mode']
        _mixins._ValueSyntax1({'name': kwargs['name']})
        _mixins._SecurityZoneModeOptions(**kwargs)
        self.type = 'SecurityZone'
        self.url = '/object/securityzones'
        if 'desc' in kwargs:
            self.desc = kwargs['desc']
        else:
            self.desc = 'Security Zone "' + self.name + '" created by API.'

        json_data = {
            "type": self.type,
            "name": self.name,
            "description": self.desc,
            "interfaceMode": self.mode,
        }
        print("Creating Security Zones.")
        print(json_data)
