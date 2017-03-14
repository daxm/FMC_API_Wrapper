# This script takes a greenfield FMC and sets it up for the FTD v6.2.1 Lab.

from fmcapi import *

# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '172.16.100.100'
username = 'apiadmin'
password = 'C1sco12345'

postdata = [
    SecurityZone(name = 'IN', desc = 'Inside Security Zone created by API', mode = 'ROUTED'),
#   example: SecurityZone() "returns": object({'objects/zones', {json_data})
    SecurityZone(name = 'OUT', desc = 'Outside Security Zone created by API', mode = 'ROUTED'),
    SecurityZone(name = 'DMZ', mode = 'ROUTED'),
    NetworkObject()
    AccessControlPolicy()
    AcpRule()
]

getdata = []
putdata = []
deletedata = []

################################# Don't mess down here #####################

with FMC(serverIP,username,password,autodeploy='False') as fmc1:
    if postdata:
        fmc1.post(postdata)
    if putdata:
        fmc1.put(putdata)
    if getdata:
        fmc1.get(getdata)
    if deletedata:
        fmc1.delete(deletedata)
