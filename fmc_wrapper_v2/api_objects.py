"""
All the API objects that I support will have a class in this file.
"""

from .helper_tools import *

# List the symbols that are exposed to the user.
__all__ = ['Network']


class Network:
    """
    Build a NetworkObject instance, sanitize its inputs (per what the FMC API will accept).
    """

    api_type = 'Network'
    api_url = 'object/networks'
    # For reference, here is the rough format of the 'exanded=true' output from the FMC NetworkObject GET request.
    template_dict = {
        'links': {
            'self': None,
            'parent': None
        },
        'type': None,
        'value': None,
        'overridable': None,
        'description': None,
        'name': None,
        'id': None,
        'metadata': {
            'readOnly': {
                'state': None,
                'reason': None,
            },
            'timestamp': None,
            'lastUser': {
                'name': None,
            },
            'domain': {
                'name': None,
                'id': None,
            },
            'ipType': None,
            'parentType': None,
        },
    }

    def __init__(self, **kwargs):
        # Cycle through kwargs and, if available, assign to instance variables.
        if 'links' in kwargs:
            self.links = kwargs['links']

        if 'value' in kwargs:
            # The FMC's 'Network' API will accept 'host' and 'range' POSTs but then you cannot
            #  retrieve them from here.  Inform the user of such.
            value_type = check_for_host_or_range(kwargs['value'])
            if value_type == 'host':
                print("Warning: value={}  Host variables are stored elsewhere."
                      "POST will work but GET won't.".format(kwargs['value']))
            elif value_type == 'range':
                print("Warning: value={}  Range variables are stored elsewhere."
                      "POST will work but GET won't.".format(kwargs['value']))

            # The 'value' value MUST be checked to ensure it matches a proper form.
            value_formatted = validate_ip_bitmask_range(kwargs['value'], value_type = value_type)
            if value_formatted['valid'] == True:
                self.value = value_formatted['value']
            else:
                print("Attribute 'value={}' provided but isn't in a usable format.".format(kwargs['value']))


        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']

        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'Created via API.'

        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'])

        if 'id' in kwargs:
            self.id = kwargs['id']

        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']

        if 'method' in kwargs:
            self.method = kwargs['method']
        else:
            self.method = 'get'

    @property
    def valid_for_post(self):
        if 'name' in self.__dict__ and 'value' in self.__dict__:
            return True
        else:
            print('ERROR: The name and value variables are required to POST.')
            return False

    @property
    def valid_for_get(self):
        return True

    @property
    def valid_for_put(self):
        if 'id' in self.__dict__:
            return True
        else:
            print('ERROR: The id variable is required to PUT.')
            return False

    @property
    def valid_for_delete(self):
        if 'id' in self.__dict__:
            return True
        else:
            print('ERROR: The id variable is required to DELETE.')
            return False

    def build_dict(self):
        # Build a valid JSON formatted data string in preparation to being sent to the FMC.
        my_dict = {}
        my_dict['type'] = self.api_type
        if 'value' in self.__dict__:
            my_dict['value'] = self.value
        if 'overridable' in self.__dict__:
            my_dict['overridable'] = self.overridable
        if 'description' in self.__dict__:
            my_dict['description'] = self.description
        if 'name' in self.__dict__:
            my_dict['name'] = self.name
        if 'id' in self.__dict__:
            my_dict['id'] = self.id
        if 'metadata' in self.__dict__:
            my_dict['metadata'] = self.metadata
        if 'links' in self.__dict__:
            my_dict['links'] = self.links
        return my_dict
