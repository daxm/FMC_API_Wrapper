"""
Misc methods/functions that are used by the api_objects.py and/or fmc.py logic.
"""

from functools import wraps
import re


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
        value_split = value.split('/')
        if value_split[1] == '32' or value_split[1] == '128':
            return 'host'
        else:
            return 'network'
    else:
        if '-' in value:
            return 'range'
        else:
            return 'host'

