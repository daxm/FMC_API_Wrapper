# This script takes a greenfield FMC and sets it up for the FTD v6.2.1 Lab.

from fmc_wrapper import CreateSecurityZone


# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '172.16.100.100'
username = 'apiadmin'
password = 'C1sco12345'

# What about the User/Pass/serverIP?  How to they get to the FMC methods?

securityzones = [
    {'name': 'IN', 'desc': 'Inside Security Zone created by API', 'mode': 'ROUTED'},
    {'name': 'OUT', 'desc': 'Outside Security Zone created by API', 'mode': 'ROUTED'},
    {'name': 'DMZ', 'desc': 'DMZ Security Zone created by API', 'mode': 'ROUTED'},
    {'name': 'asdf', 'desc': 'asdf', 'mode': 'TRANSPARENT'},
]

for zone in securityzones:
    CreateSecurityZone(name=zone['name'], mode=zone['mode'], desc=zone['desc'])
# But what if I don't want to set a description on every one of them?  Hmmm.

# What about deployment?  We don't want to deploy after each of the above statements
#  but rather at the end of the script (assuming we don't disable autodeploy).

