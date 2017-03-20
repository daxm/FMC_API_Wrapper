# This script takes a greenfield FMC and sets it up for the FTD Basics Lab.

from fmc_wrapper import *

# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '64.100.10.13'
username = 'apiadmin'
password = 'Admin123'

# The example values shown here are from "FTD Basics" lab that is hosted on dCloud.
accesscontrolpolicies = [
    AccessControlPolicy(name='Base', defaultAction='BLOCK'),
    AccessControlPolicy(name='HQ', defaultAction='BLOCK'),
    AccessControlPolicy(name='Remote Locations', defaultAction='BLOCK'),
]

"""
accesscontrolpolicyrules = [
    AccessControlPolicyRule(name='INET Access', acpname='Base', action='ALLOW', sourceNetwork='HQLAN', destNetwork='any-ipv4'),
    AccessControlPolicyRule(name='Access FMC', acpname='HQ', action='ALLOW', sourceNetwork='any-ipv4', destNetwork='FMC_Private'),
    AccessControlPolicyRule(name='Block Facebook', acpname='Base', action='BLOCK', sourceNetwork='ExampleCorpLANs', destNetwork='any-ipv4', urlObject='Facebook'),
    AccessControlPolicyRule(name='Permit Facebook', acpname='HQ', action='ALLOW', sourceNetwork='HQLAN', destNetwork='any-ipv4', urlObject='Facebook'),
    AccessControlPolicyRule(name='Block gambling.com', acpname='Base', action='BLOCK', sourceNetwork='ExampleCorpLANs', destNetwork='any-ipv4', urlObject='gambling.com'),
    AccessControlPolicyRule(name='Block 888.com', acpname='Base', action='BLOCK', sourceNetwork='ExampleCorpLANs', destNetwork='any-ipv4', urlObject='888.com'),
]

devices = [
    Device(name='HQ-FTD', hostname='172.16.100.10', acpname='HQ', regkey='cisco123', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
    Device(name='REMOTE1-FTD', hostname='198.18.2.10', acpname='Remote Locations', regkey='cisco123', natid='12345', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
    Device(name='REMOTE2-FTD', acpname='Remote Locations', regkey='cisco123', natid='a1b2', license_caps=['MALWARE', 'URLFilter', 'THREAT']),
]
"""

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

with FMC(serverIP,username,password,autodeploy=False) as fmc1:
    pass

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

# for sz in (securityzones + accesscontrolpolicies + accesscontrolpolicyrules + devices + networkobjects + urlobjects):
#    print(sz)
