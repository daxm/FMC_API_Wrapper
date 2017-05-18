import datetime
import requests
import sys
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from .helper_tools import *

@logger
class FMC(object):
    """
    This class contains the methods used when interacting with the FMC.
    Mainly around establishing and maintaining the connection and performing any Method actions (get, put, post, delete).
    """

    API_PLATFORM_VERSION = '/api/fmc_platform/v1/'
    API_CONFIG_VERSION = '/api/fmc_config/v1/'
    VERIFY_CERT = False
    TOKEN_LIFETIME = 60 * 30

    def __init__(self, host, username='admin', password='Admin123', autodeploy=True):
        self.host = host
        self.username = username
        self.password = password
        self.autodeploy = autodeploy

        self.headers = {'Content-Type': 'application/json'}
        self.token_expiry = None
        self.token = None
        self.refreshtoken = None
        self.token_refreshes = None
        self.uuid = None
        self.base_url = None

        if not self.VERIFY_CERT:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        if self.autodeploy:
            self.deploychanges()
        else:
            print('Auto Deploy is disabled.\n'
                  'Set "autodeploy=True" if you want this script to push changes to its managed devices.\n')

    def reset_token_expiry(self):
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.TOKEN_LIFETIME)

    def refresh_token(self):
        self.headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token,
                        'X-auth-refresh-token': self.refreshtoken}
        url = "https://" + self.host + self.API_PLATFORM_VERSION + "auth/refreshtoken"
        print("Refreshing token from %s.\n" % url)
        response = requests.post(url, headers=self.headers, verify=self.VERIFY_CERT)
        self.token_refreshes += 1
        self.reset_token_expiry()
        self.token = self.headers.get('X-auth-access-token')
        self.refreshtoken = self.headers.get('X-auth-refresh-token')
        self.headers['X-auth-access-token'] = self.token

    def connect(self):
        # define fuction to connect to the FMC API and generate authentication token
        # Token is good for 30 minutes.
        url = "https://" + self.host + self.API_PLATFORM_VERSION + "auth/generatetoken"
        print("Requesting token from %s." % url)
        response = requests.post(url, headers=self.headers,
                                 auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                                 verify=self.VERIFY_CERT)

        self.token = response.headers.get('X-auth-access-token')
        self.refreshtoken = response.headers.get('X-auth-refresh-token')
        self.uuid = response.headers.get('DOMAIN_UUID')
        if self.token is None or self.uuid is None:
            print("No Token or DOMAIN_UUID found, terminating....")
            sys.exit()
        self.base_url = "https://" + self.host + self.API_CONFIG_VERSION + "domain/" + self.uuid
        self.reset_token_expiry()
        self.token_refreshes = 0

        print("Token creation a success -->", self.token, "which expires ", self.token_expiry, "\n")

    def checktoken(self):
        if datetime.datetime.now() > self.token_expiry:
            print("Token Expired.  Generating new token.\n")
            self.connect()

    def getdeployabledevices(self):
        waittime = 15
        print("Waiting %s seconds to allow the FMC to update the list of deployable devices." % waittime)
        time.sleep(waittime)
        print("Getting a list of deployable devices.")
        url = "/deployment/deployabledevices?expanded=true"
        response = self.send_to_api(url=url, json_data='')
        # Now to parse the response list to get the UUIDs of each device.
        if 'items' not in response:
            return
        uuids = []
        for item in response['items']:
            if not item['canBeDeployed']:
                pass
            else:
                uuids.append(item['device']['id'])
        return uuids

    def deploychanges(self):
        url = "/deployment/deploymentrequests"
        devices = self.getdeployabledevices()
        if not devices:
            print("No devices need deployed.")
            return
        nowtime = int(1000 * datetime.datetime.now().timestamp())
        json_data = {'type': 'DeploymentRequest', 'forceDeploy': True, 'ignoreWarning': True, 'version': nowtime,
            'deviceList': []}
        for device in devices:
            print("Adding device %s to deployment queue." % device)
            json_data['deviceList'].append(device)
        print("Deploying changes to devices.")
        response = self.send_to_api(url=url, json_data=json_data)
        return response['deviceList']

    def send_to_api(self, **kwargs):
        self.checktoken()
        # POST json_data with the REST CALL
        try:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
            url = self.base_url + '/' + kwargs['url']

            if kwargs['method'] == 'post':
                response = requests.post(url, json=kwargs['json_data'], headers=headers, verify=self.VERIFY_CERT)
            elif kwargs['method'] == 'get':
                url = url
                if 'id' in kwargs['json_data']:
                    url = url + "/" + kwargs['json_data']['id']
                else:
                    url = url + "?expanded=true"
                response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
            elif kwargs['method'] == 'put':
                pass
            elif kwargs['method'] == 'delete':
                pass

            status_code = response.status_code
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error in POST operation -->", str(err))
            print("json_response -->\t", json_response)
        if response:
            response.close()
        return json_response

    def configure(self, users_objects):
        for obj in users_objects:
            do_action = False
            if obj.method == 'post':
                if obj.valid_for_post:
                    do_action = True
            elif obj.method == 'get':
                if 'name' in obj.__dict__:
                    """
                    Alas, you have to "getall" and parse through looking for the specific entry to get the ID.
                    Then you have to use "get" using the ID.
                    """
                    results = self.send_to_api(method='get', url=obj.api_url, json_data='')
                    for item in results['items']:
                        if item['name'] == obj.name:
                            obj.id = item['id']
                    if 'id' not in obj.__dict__:
                        print("ERROR: Cannot find item with name {} in {}.".format(obj.name, obj.__class__))
                    else:
                        do_action = True
                else:
                    do_action = True
            elif obj.method == 'put':
                if obj.valid_for_put:
                    do_action = True
            elif obj.method == 'delete':
                if 'name' in obj.__dict__:
                    pass
                if obj.valid_for_delete:
                    do_action = True
            if do_action:
                results = self.send_to_api(method=obj.method, url=obj.api_url, json_data=obj.build_dict())
                print("Method:{}, Results:{}\n".format(obj.method, results))
            else:
                print('ERROR: Method: "{}" failed to run for {}\n'.format(obj.method, obj.__class__))
