from .decorate import logger, syntax_correcter

"""
All the API objects that I support will have a class in this file.
"""


class NetworkObject:
    """
    Build a NetworkObject instance, sanitize its inputs (per what the FMC API will accept).
    """

    api_type = 'Network'
    api_url = 'object/networks'
    # Here is the rough format of the 'exanded=true' output from the FMC NetworkObject GET request.
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
            self.value = kwargs['value']

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

    @property
    def valid_for_post(self):
        if 'name' in self.__dict__ and 'value' in self.__dict__:
            return True
        else:
            print('ERROR: The name and value variables are required to POST.')
            return False

    @property
    def valid_for_get(self):
        if 'id' in self.__dict__:
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

    @property
    def valid_for_getall(self):
        return True

    def create_json(self):
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
        return my_dict

    def get_id(self):
        pass
