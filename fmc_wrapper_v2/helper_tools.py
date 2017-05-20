"""
Misc methods/functions that are used by the api_objects.py and/or fmc.py logic.
"""

from functools import wraps
import re
import ipaddress
import json

def logger(orig_function):
    """
    Create/Modify a log file with the name of the orig_function.
    Log the args and kwargs to the file as INFO.
    :param orig_function: 
    :return: decorated orig_function 
    """

    import logging
    logging.basicConfig(filename='logs/troubleshooting.log'.format(orig_function.__name__), level=logging.INFO)

    @wraps(orig_function)
    def wrapper(*args, **kwargs):
        logging.info('{} has args: {}, and kwargs: {}'.format(orig_function.__name__, args, kwargs))
        return orig_function(*args, **kwargs)

    return wrapper


def syntax_correcter(value, permitted_syntax="[.\w\d_\-]", replacer='_'):
    """
    Check 'value' for invalid characters (identified by 'permitted_syntax') and replace them with 'replacer'.
    :param value:  String to be checked.
    :param permitted_syntax: (optional) regex of allowed characters.
    :param replacer: (optional) character used to replace invalid characters.
    :return: Modified string with "updated" characters.
    """
    new_value = ''
    for char in range(0, len(value)):
        if not re.match(permitted_syntax, value[char]):
            new_value += replacer
        else:
            new_value += value[char]
    return new_value


def check_for_host_or_range(value):
    """
    Check to see whether 'value' is a host, range, or network.
    :param value: 
    :return: 
    """
    if '/' in value:
        ip, bitmask = value.split('/')
        if ip == '32' or bitmask == '128':
            return 'host'
        else:
            return 'network'
    else:
        if '-' in value:
            return 'range'
        else:
            return 'host'


def is_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError as err:
        print(err)
        return False
    return True


def is_ip_network(ip):
    try:
        ipaddress.ip_network(ip)
    except ValueError as err:
        print(err)
        return False
    return True


def validate_ip_bitmask_range(value, value_type):
    """
    We need to check the provided IP address (or range of addresses) and make sure the IPs are valid.
    :param value: IP, IP/Bitmask, or IP Range
    :param value_type: 
    :return: dict {value=value_fixed, valid=boolean}
    """
    return_dict = {'value': value, 'valid': False}
    if value_type == 'range':
        for ip in value.split('-'):
            if is_ip(ip):
                return_dict['valid'] = True
    elif value_type == 'host' or value_type == 'network':
        if is_ip_network(value):
            return_dict['valid'] = True
    return return_dict

def mocked_requests_get(**kwargs):
    class MockResponse:
        def __init__(self, **kwargs):
            self.text = json.dumps(kwargs['text'])
            self.status_code = kwargs['status_code']

        def close(self):
            return True
    return MockResponse(**kwargs)
