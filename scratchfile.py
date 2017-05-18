from fmc_wrapper_v2 import FMC
from fmc_wrapper_v2 import config

"""
Open a connection to FMC.  Optionally choose whether to deploy to FTDs once connection is closed.
"""
with FMC(config.serverIP, config.username, config.password, autodeploy= config.autodeploy) as fmc1:
    for obj in config.users_objects:
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

            obj.method = 'get'
            do_action = True

        if do_action:
            results = fmc1.send(method = obj.method, url=obj.api_url, json_data=obj.create_json())
            print("Method:{}, Results:{}\n".format(obj.method,results))
        else:
            print('ERROR: Method: "{}" failed to run for {}\n'.format(obj.method, obj.__class__))

print('Connection to FMC is now exited.  Thank you for playing.')
