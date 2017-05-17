from fmc_wrapper_v2.api_objects import *
from fmc_wrapper_v2 import FMC

# Set FMC IP, Username, Password.
username = 'apiscript'
password = 'Admin123'
serverIP = '192.168.11.5'

# Open a connection to FMC.  Optionally choose whether to deploy to FTDs once connection is closed.
with FMC(serverIP, username, password, autodeploy=False) as fmc1:

    # Testing Area #
    test_dict = {}
    test_dict['name'] = 'Dax Mickelson'
    test_dict['age'] = 4
    test_dict['validate'] = True

    my_network_object1 = NetworkObject(**test_dict)
    test_dict['value'] = '1.2.3.4/24'
    my_network_object2 = NetworkObject(**test_dict)

    # print(my_network_object1.valid_for_post())
    # print(my_network_object2.valid_for_post())

    print(my_network_object1.name)

    fmc1.get(NetworkObject(**test_dict))
