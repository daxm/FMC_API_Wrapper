# This script takes a greenfield FMC and sets it up for the FTD v6.2.1 Lab.

import fmc_wrapper.SecurityZone

# ############################# User Created Variables to be used below functions ############################
# FMC Server Info.
serverIP = '172.16.100.100'
username = 'apiadmin'
password = 'C1sco12345'

### What about the User/Pass/serverIP?  How to they get to the FMC methods?
fmc_wrapper.SecurityZone.SecurityZone(name = 'IN', mode = 'ROUTED')
fmc_wrapper.SecurityZone.SecurityZone(name = 'OUT', mode = 'ROUTED')
fmc_wrapper.SecurityZone.SecurityZone(name = 'DMZ', mode = 'ROUTED', desc = 'DMZ Zone, but not used in the lab.')
