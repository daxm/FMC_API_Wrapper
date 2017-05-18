from .api_objects import *
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
    NetworkObject(method='post', name='Dax Mickelson', value='1.2.3.4/32',),
    NetworkObject(method='post', name='Alpha^^Beta%%Cappa', value='2.2.3.0/24',),
    NetworkObject(method='getall',),
    NetworkObject(method='get', name='Dax_Mickelson',),
]
