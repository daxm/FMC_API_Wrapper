from fmc_wrapper_v2.api_objects import *
from fmc_wrapper_v2 import FMC
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
    NetworkObject(method='post', name='A Dax Mickelson', value='1.2.3.4/32'),
    NetworkObject(method='post', name='A**B@d^MoJo!!', value='2.3.4.0/24'),
    NetworkObject(method='getall', name='daxmShop'),
    NetworkObject(method='get', id='000C2926-64BB-0ed3-0000-012884901891'),
    NetworkObject(method='getbyname', name='daxmShop'),
]

"""
Open a connection to FMC.  Optionally choose whether to deploy to FTDs once connection is closed.
"""
with FMC(serverIP, username, password, autodeploy = autodeploy) as fmc1:
    for obj in users_objects:
        do_action = False
        if obj.method == 'post':
            if obj.valid_for_post:
                do_action = True
        elif obj.method == 'get':
            if obj.valid_for_get:
                do_action = True
        elif obj.method == 'put':
            if obj.valid_for_put:
                do_action = True
        elif obj.method == 'delete':
            if obj.valid_for_delete:
                do_action = True
        elif obj.method == 'getall':
            if obj.valid_for_getall:
                do_action = True
        elif obj.method == 'getbyname':
            """
            Alas, you have to "getall" and parse through looking for the specific entry to get the ID.
            Then you have to use "get" using the ID.
            """
            results = fmc1.send(method = 'getall', url = obj.api_url, json_data='')
            for item in results['items']:
                if item['name'] == obj.name:
                    obj.id = item['id']
                    do_action = True
                    obj.method = 'get'
            if do_action == False:
                print("ERROR: Cannot find item with name {} in {}.".format(obj.name, obj.__class__))
        if do_action:
            results = fmc1.send(method = obj.method, url=obj.api_url, json_data=obj.create_json())
            print("Method:{}, Results:{}\n".format(obj.method,results))
        else:
            print('ERROR: Method: "{}" failed to run for {}\n'.format(obj.method, obj.__class__))

print('Connection to FMC is now exited.  Thank you for playing.')
