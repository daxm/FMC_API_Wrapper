import datetime
import json
import requests
import sys
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .api_objects import *



"""
Firepower Management Center API wrapper class for managing Firepower Threat Defense and legacy Firepower devices through a Firepower Management Center

http://www.cisco.com/c/en/us/td/docs/security/firepower/610/api/REST/Firepower_REST_API_Quick_Start_Guide/Objects_in_the_REST_API.html
 
"""

class FMC(object):
    """
    FMC objects
    """
    
    API_PLATFORM_VERSION = '/api/fmc_platform/v1/'
    API_CONFIG_VERSION =  '/api/fmc_config/v1/'
    VERIFY_CERT = False
    TOKEN_LIFETIME = 60 * 30
    
    def __init__(self, host, username='admin', password='Admin123', autodeploy=True):
        self.host = host
        self.username = username
        self.password = password
        self.autodeploy = autodeploy

        if not self.VERIFY_CERT:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, *args):
        if self.autodeploy:
            self.deploychanges()
        else:
            print('Auto Deploy is disabled.  Set "autodeploy=True" if you want this script to push changes to its managed devices.')

    def reset_token_expiry(self):
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.TOKEN_LIFETIME)

    def refresh_token(self):
        self.headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token, 'X-auth-refresh-token': self.refreshtoken }
        self.url = "https://" + self.host + self.API_PLATFORM_VERSION + "auth/refreshtoken"
        print("Refreshing token from %s." % self.url)
        self.response = requests.post(self.url, headers=self.headers, verify=self.VERIFY_CERT)
        self.token_refreshes += 1
        self.reset_token_expiry()
        self.token = self.headers.get('X-auth-access-token')
        self.refreshtoken = self.headers.get('X-auth-refresh-token')
        self.headers['X-auth-access-token'] = self.token
        
    def connect(self):
        # define fuction to connect to the FMC API and generate authentication token
        # Token is good for 30 minutes.
        self.headers = {'Content-Type': 'application/json'}
        self.url = "https://" + self.host + self.API_PLATFORM_VERSION + "auth/generatetoken"
        print("Requesting token from %s." % self.url)
        self.response = requests.post(self.url, headers=self.headers, auth=requests.auth.HTTPBasicAuth(self.username, self.password), verify=self.VERIFY_CERT)

        self.token = self.response.headers.get('X-auth-access-token')
        self.refreshtoken = self.response.headers.get('X-auth-refresh-token')
        self.uuid = self.response.headers.get('DOMAIN_UUID')
        if self.token is None or self.uuid is None:
            print("No Token or DOMAIN_UUID found, terminating....")
            sys.exit()
            
        self.base_url = "https://" + self.host + self.API_CONFIG_VERSION + "domain/" + self.uuid
        self.reset_token_expiry()
        self.token_refreshes = 0
            
        print("Token creation a success -->", self.token, "which expires ", self.token_expiry)

    def checktoken(self):
        if datetime.datetime.now() > self.token_expiry:
            print("Token Expired.  Generating new token.")
            self.connect()

    def get(self, obj_list):
        self.checktoken()
        # GET requested data and return it.
        for object in obj_list:
            try:
                self.headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
                self.url = self.base_url + "/" + object.api_url
                self.response = requests.get(self.url, headers=self.headers, verify=self.VERIFY_CERT)
                self.status_code = self.response.status_code
                self.json_response = json.loads(self.response.text)
                if self.status_code > 301 or 'error' in self.json_response:
                    self.response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print("Error in GET operation -->", str(err))
                print("json_response -->\t", self.json_response)
            print(self.json_response)
            if self.response:
                self.response.close()
            return self.json_response

    def postdata(self, url, json_data):
        self.checktoken()
        # POST json_data with the REST CALL
        try:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
            url = self.base_url + url
            response = requests.post(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
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

    def putdata(self, url, json_data):
        self.checktoken()
        # PUT json_data with the REST CALL
        try:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
            url = self.base_url + url
            response = requests.put(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
            status_code = response.status_code
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error in PUT operation -->", str(err))
            print("json_response -->\t", json_response)
        if response:
            response.close()
        return json_response

    def getdeployabledevices(self):
        waittime = 15
        print("Waiting %s seconds to allow the FMC to update the list of deployable devices." % waittime)
        time.sleep(waittime)
        print("Getting a list of deployable devices.")
        url = "/deployment/deployabledevices?expanded=true"
        response = self.getdata(url)
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
        json_data = {
            'type': 'DeploymentRequest',
            'forceDeploy': True,
            'ignoreWarning': True,
            'version': nowtime,
            'deviceList': []
        }
        for device in devices:
            print("Adding device %s to deployment queue." % device)
            json_data['deviceList'].append(device)
        print("Deploying changes to devices.")
        response = self.postdata(url, json_data)
        return response['deviceList']

