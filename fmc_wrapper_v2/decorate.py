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

# OLD SHIT #
def timer(orig_function):
    """
    Calculate the time the orig_function took to run.
    :param orig_function: 
    :return: decorated orig_function
    """

    import time

    @wraps(orig_function)
    def wrapper(*args, **kwargs):
        starttime = time.time()
        result = orig_function(*args, **kwargs)
        endtime = time.time()
        print('{} ran in: {} sec'.format(orig_function.__name__, endtime - starttime))
        return result

    return wrapper


def syntaxcheck_name(orig_function):
    permitted_syntax = "^[\w\d][.\w\d_\-]*$"

    @wraps(orig_function)
    def wrapper(*args, **kwargs):
        if not re.match(permitted_syntax, kwargs['name']):
            print("Invalid character used in: %s" % (kwargs['name']))
            raise KeyError()
        orig_function(*args, **kwargs)

    return wrapper


def syntax_checker(value, permitted_syntax="^[\w\d][.\w\d_\-]*$"):
    """
    Checks the value variable for permitted_syntax values.  If it fails, print an error and return False, otherwise
    return True.
    :param value: string to be checked for allowed values 
    :param permitted_syntax: regex of allowed values
    :return: True or False, depending.
    """

    if not re.match(permitted_syntax, value):
        raise ValueError("Invalid character used in: %s" % value)
        return False
    else:
        return True

