"""
Essentially this file is the FMC class and its methods.
"""

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
    Mainly around establishing and maintaining the connection and performing
     any Method actions (get, put, post, delete).
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
        requests.post(url, headers=self.headers, verify=self.VERIFY_CERT)
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
        json_data = {'type': 'DeploymentRequest', 'forceDeploy': True, 'ignoreWarning': True,
                     'version': nowtime, 'deviceList': []}
        for device in devices:
            print("Adding device %s to deployment queue." % device)
            json_data['deviceList'].append(device)
        print("Deploying changes to devices.")
        response = self.send_to_api(url=url, json_data=json_data)
        return response['deviceList']

    @property
    def validate_data(self):
        if self.obj.method == 'post':
            return self.obj.valid_for_post
        if self.obj.method == 'put':
            return self.obj.valid_for_put
        if self.obj.method == 'delete':
            return self.obj.valid_for_delete
        if self.obj.method == 'get':
            return self.obj.valid_for_get

    def send_to_api(self, **kwargs):
        self.checktoken()
        response = None
        json_response = None
        # POST json_data with the REST CALL
        try:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
            url = self.base_url + '/' + kwargs['url']
            if kwargs['method'] == 'get':
                if 'id' in kwargs['json_data']:
                    url = url + "/" + kwargs['json_data']['id']
                else:
                    url = url + "?expanded=true&limit=1000"
            status_code = 429
            while status_code == 429:
                if kwargs['method'] == 'post':
                    response = requests.post(url, json=kwargs['json_data'], headers=headers, verify=self.VERIFY_CERT)
                elif kwargs['method'] == 'get':
                    response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
                elif kwargs['method'] == 'put':
                    response = requests.put(url, headers=headers, verify=self.VERIFY_CERT)
                elif kwargs['method'] == 'delete':
                    response = requests.delete(url, headers=headers, verify=self.VERIFY_CERT)
                status_code = response.status_code
                if status_code == 429:
                    waittime = 60
                    print("Sending too many requests to the FMC too fast.  Waiting {} seconds and trying again.".format(waittime))
                    time.sleep(waittime)
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error in POST operation -->", str(err))
            print("json_response -->\t", json_response)
        if response:
            response.close()
        return json_response

    def analyze_get_results(self, results):
        for item in results['items']:
            if 'id' in self.obj.__dict__:
                if item['id'] == self.obj.id:
                    self.accumulated_results = results
                    return True
            elif 'name' in self.obj.__dict__:
                if item['name'] == self.obj.name:
                    self.obj.id = item['id']
                    self.accumulated_results = results
                    return True
            else:
                return False

    def search_api_paths(self):
        self.accumulated_results = []
        for path in self.obj.search_api_paths:
            results = self.send_to_api(method='get', url=path, json_data='')
            if 'id' in self.obj.__dict__ or 'name' in self.obj.__dict__:
                self.obj.api_url = path
                if self.analyze_get_results(results):
                    break
            else:
                # Enter here is "getall" is requested.  (Which is essentially if 'id' nor 'name' are present.)
                
        return self.accumulated_results

    def configure(self, users_objects):
        for self.obj in users_objects:
            if self.validate_data:
                # take action (i.e. interact with FMC)
                if self.obj.method == 'get':
                    """
                    The 'get' method is a pain since it needs to possibly be run against multiple API paths.  (You
                     can 'post' using one api_path but the data is actually moved/stored in another path (and is only
                      accessible via that path).)
                    'get' either "all" or find data based on 'name' or 'id'.
                    
                    """
                    results = self.search_api_paths()
                else:
                    results = self.send_to_api(method=self.obj.method, url=self.obj.api_url, json_data=self.obj.build_dict())
                print("Method:{}, Results:{}\n".format(self.obj.method, results))
            else:
                # Whine and cry.
                print('ERROR: Method: "{}" failed to run for {}\n'.format(self.obj.method, self.obj.__class__))
