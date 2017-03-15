# This script takes a greenfield FMC and sets it up for the FTD Basics Lab.

from fmc_wrapper import *


print(SecurityZone(name='IN', description='Inside Security Zone created by API', mode='ROUTED'))
# print(SecurityZone(name='_IN', description='Inside Security Zone created by API', mode='ROUTED'))
# print(SecurityZone(name='IN ', description='Inside Security Zone created by API', mode='ROUTED'))
# print(SecurityZone(name='IN', mode='ROUTED'))
# print(SecurityZone(name='IN', description='Inside Security Zone created by API', mode='RUTED'))
# print(SecurityZone(name='IN', description='Inside Security Zone created by API', mode='TRANSPARENT'))
# print(SecurityZone(name='OUT', description='Outside Security Zone created by API', mode='TRANSPARENT'))
# print(dir(SecurityZone))
# help(SecurityZone)

json_data = """{
  "name": "SecurityZoneObject5",
  "description": "Sec-zone-UUID-1",
  "type": "SecurityZone",
  "mode": "ROUTED"
}
"""

sz = SecurityZone.from_json(json_data)
print(sz)
exit()

# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '172.16.100.100'
username = 'apiadmin'
password = 'C1sco12345'

# The example values shown here are from "FTD Basics" lab that is hosted on dCloud.
accesscontrolpolicies = [
    AccessControlPolicy(name='Base', defaultaction='BLOCK'),
    AccessControlPolicy(name='HQ', defaultaction='BLOCK'),
    AccessControlPolicy(name='Remote Locations', defaultaction='BLOCK'),
]

accesscontrolpolicyrules = [
    AccessControlPolicyRule(name='INET Access', acpname='Base', action='PERMIT', sourcenetwork='HQLAN', destnetwork='any-ipv4'),
    AccessControlPolicyRule(name='Access FMC', acpname='HQ', action='PERMIT', sourcenetwork='any-ipv4', destnetwork='FMC_Private'),
    AccessControlPolicyRule(name='Block Facebook', acpname='Base', action='BLOCK', sourcenetwork='ExampleCorpLANs', destnetwork='any-ipv4', urlobject='Facebook'),
    AccessControlPolicyRule(name='Permit Facebook', acpname='HQ', action='PERMIT', sourcenetwork='HQLAN', destnetwork='any-ipv4', urlobject='Facebook'),
    AccessControlPolicyRule(name='Block gambling.com', acpname='Base', action='BLOCK', sourcenetwork='ExampleCorpLANs', destnetwork='any-ipv4', urlobject='gambling.com'),
    AccessControlPolicyRule(name='Block 888.com', acpname='Base', action='BLOCK', sourcenetwork='ExampleCorpLANs', destnetwork='any-ipv4', urlobject='888.com'),
]

devices = [
    Device(name='HQ-FTD', hostname='172.16.100.10', acpname='HQ', regkey='cisco123', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
    Device(name='REMOTE1-FTD', hostname='198.18.2.10', acpname='Remote Locations', regkey='cisco123', natid='12345', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
    Device(name='REMOTE2-FTD', acpname='Remote Locations', regkey='cisco123', natid='a1b2', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
]

networkobjects = [
    NetworkObject(name='HQLAN', value='172.16.100.0/24'),
    NetworkObject(name='ExampleCorpNETs', value='172.16.0.0/16'),
    NetworkObject(name='Remote1LAN', value='172.16.103.0/24'),
    NetworkObject(name='Remote2LAN', value='172.16.105.0/24'),
    NetworkObject(name='FMC_Public', value='198.18.1.100'),
    NetworkObject(name='FMC_Private', value='172.16.100.100'),
    NetworkObject(name='DMZServer_Public', value='198.18.1.50'),
    NetworkObject(name='DMZServer_Private', value='172.16.101.50'),
]

securityzones = [
    SecurityZone(name='IN', description='Inside Security Zone created by API', mode='ROUTED'),
    SecurityZone(name='OUT', description='Outside Security Zone created by API', mode='ROUTED'),
    SecurityZone(name='DMZ', mode='ROUTED'),
]

urlobjects = [
    UrlObject(name='Cisco', value='www.cisco.com'),
    UrlObject(name='Facebook', value='facebook.com'),
    UrlObject(name='daxm', value='daxm.net'),
    UrlObject(name='gambling.com', value='gambling.com'),
    UrlObject(name='888.com', value='888.com'),
]

# ################################ Main Program Logic Below Here #####################

# with FMC(serverIP,username,password,autodeploy='False') as fmc1:
"""
Recommended order to do things: delete, post, put, get
Also, order in which you do things is important.  Don't try to add an Access Control Policy Rule before you
create the Access Control Policy to which it associated.

Remember that whitespace is important in python and the commands listed below need to be indented
the same since they are "within" the with statement above.  Uncomment whichever of the following lines to test.

Examples of using this script:
"""
#    fmc1.post(securityzones)
#    fmc1.post(urlobjects)
#    fmc1.post(networkobjects)
#    fmc1.post(accesscontrolpolicies)
#    fmc1.post(accesscontrolpolicyrules)
#    fmc1.post(devices)

#    fmc1.delete(securityzones)
#    fmc1.put(NetworkObjects)
#    fmc1.get(SecurityZones)

"""
uuidfield = UuidField()
uuidfield.uuid = '123e4567-e89b-12d3-a456-426655440000'
print(uuidfield.uuid)
daxuuid = uuidfield.uuid
print(daxuuid)
"""
for sz in securityzones:
    print(sz)
