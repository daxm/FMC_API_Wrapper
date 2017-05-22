"""
Firepower Management Center API wrapper class for managing Firepower Threat Defense and legacy Firepower
 devices through a Firepower Management Center.

http://www.cisco.com/c/en/us/td/docs/security/firepower/610/api/REST/
 Firepower_REST_API_Quick_Start_Guide/Objects_in_the_REST_API.html
 
"""

from .fmc import *
from .api_objects import *
__all__ = (fmc.__all__ + api_objects.__all__)
