import datetime
import json
import requests
import sys
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_VERSION = '/api/fmc_platform/v1/'
VERIFY_CERT = False
TOKEN_LIFETIME = 60 * 30

__all__=['PostData', 'PutData', 'GetData']

def __init__(self, host, username='admin', password='Admin123', autodeploy=True):
    self.host = host
    self.username = username
    self.password = password
    self.autodeploy = autodeploy
    print("%s/%s/%s/%s" % (self.host, self.username, self.password, self.autodeploy))


def __enter__(self):
    self.connect()
    return self


def __exit__(self, *args):
    if self.autodeploy:
        self.deploychanges()


def reset_token_expiry(self):
    self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_LIFETIME)


def refresh_token(self):
    headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token,
               'X-auth-refresh-token': self.refreshtoken}
    url = "https://" + self.host + self.API_VERSION + "auth/refreshtoken"
    print("Refreshing token from %s." % url)
    response = requests.post(url, headers=headers, verify=self.VERIFY_CERT)
    self.token_refreshes += 1
    self.reset_token_expiry()
    self.token = self.headers.get('X-auth-access-token')
    self.refreshtoken = self.headers.get('X-auth-refresh-token')
    self.headers['X-auth-access-token'] = self.token


def connect(self):
    # define fuction to connect to the FMC API and generate authentication token
    # Token is good for 30 minutes.
    headers = {'Content-Type': 'application/json'}
    url = "https://" + self.host + self.API_VERSION + "auth/generatetoken"
    print("Requesting token from %s." % url)
    response = requests.post(url, headers=headers, auth=requests.auth.HTTPBasicAuth(self.username, self.password),
                             verify=self.VERIFY_CERT)

    self.token = self.headers.get('X-auth-access-token')
    self.refreshtoken = self.headers.get('X-auth-refresh-token')
    self.uuid = self.headers.get('DOMAIN_UUID')
    if self.token is None or self.uuid is None:
        print("No Token or DOMAIN_UUID found, terminating....")
        sys.exit()

    self.base_url = "https://" + self.host + self.API_VERSION + "domain/" + self.uuid
    self.reset_token_expiry()
    self.token_refreshes = 0

    print("Token creation a success -->", token, "which expires ", self.token_expiry)


def checktoken(self):
    if datetime.datetime.now() > self.token_expiry:
        print("Token Expired.  Generating new token.")
        self.connect()


class PostData(object):
    """
    Issue a POST action on the FMC with the passed JSON formatted data.
    """


    def __init__(self):
        pass
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


class PutData(object):
    pass
    """
    Totally not working right now.
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
    # return json_response
    """


class GetData(object):
    pass
    """
    Totally not working now.
    self.checktoken()
    # GET requested data and return it.
    try:
        headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.token}
        url = self.base_url + url
        response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
        status_code = response.status_code
        json_response = json.loads(response.text)
        if status_code > 301 or 'error' in json_response:
            response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Error in GET operation -->", str(err))
        print("json_response -->\t", json_response)
    if response:
        response.close()
    # return json_response
    """

