from fmc_wrapper_v2.api_objects import *
from fmc_wrapper_v2.fmc import FMC
import sys

"""
Set FMC IP, Username, Password.
"""
username = 'apiscript'
password = 'Admin123'
serverIP = '192.168.11.5'
autodeploy = False

# Use passed in username password, if so desired.
if len(sys.argv) > 2:
    username = sys.argv[1]
    password = sys.argv[2]

"""
Create a list of python objects relating to the various API objects.
Set the method for each object (get, post, put, delete, getall) and any data you wish to send.
For now, any 'get' method will just print data to the screen.  The other methods will print a success message
 or a reason for failure.
"""

users_objects = [
    Network(method='get',),
    Network(method='get', id='000C2926-64BB-0ed3-0000-012884901891'),
    Network(method='get', name='daxmShop'),
    Network(),
]

#users_objects = [
#    Network(method='delete', id='000C2926-64BB-0ed3-0000-012884906404'),
#    Network(method='delete', name='A Dax Mickelson')
#]

"""
Open a connection to FMC.  Optionally choose whether to deploy to FTDs once connection is closed.
"""
with FMC(serverIP, username, password, autodeploy = autodeploy) as fmc1:
    fmc1.configure(users_objects)

print('Connection to FMC is now exited.  Thank you for playing.')
