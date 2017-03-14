from . import export
from . import _mixins


@export
class NetworkObjects(_NameRequired, _ModeValidate, object):
    pass

