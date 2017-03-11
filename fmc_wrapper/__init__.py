"""
Firepower Management Center API wrapper for managing Firepower Threat Defense and legacy Firepower devices through a Firepower Management Center

http://www.cisco.com/c/en/us/td/docs/security/firepower/610/api/REST/Firepower_REST_API_Quick_Start_Guide/Objects_in_the_REST_API.html

Currently tested against FMC v6.2.0
"""

from .SecurityZone import *
from .NetworkObject import *


__all__ = (SecurityZone.__all__ + NetworkObject.__all__)
