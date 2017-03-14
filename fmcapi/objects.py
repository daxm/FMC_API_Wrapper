"""
FMC API Rest Objects

"""
from object_mixins import NameField,NameWithSpaceField,ModeField

class SecurityZone(ModeField, NameField, UuidField):
    version = 1

class NetworkObject(ModeField, NameField, UuidField):
    version = 1

-----------------------------------------

from fmcapi import FMC
from fmcapi.objects import SecurityZone

stuff_to_post = [
    SecurityZone(name="asdf", mode="ROUTED"),
    NetworkObject(name=" asdf1", mode="ROUTED"),
]

with FMC(host='1.3.4.5',username='admin',password='pass') as fmc1:
  fmc1.post(stuff_to_post)

-----------------------------------------



