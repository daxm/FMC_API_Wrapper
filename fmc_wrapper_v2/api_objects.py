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

    def __init__(self, **kwargs):
        # Cycle through kwargs and, if available, assign to instance variables.
        if 'links' in kwargs:
            self.links = kwargs['links']

        if 'value' in kwargs:
            self.value = kwargs['value']

        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']
        else:
            self.overridable = False

        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'Created via API.'

        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'], permitted_syntax="[.\w\d_\- ]")

        if 'id' in kwargs:
            self.id = kwargs['id']

        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']

    @property
    def valid_for_post(self):
        # The variables 'name' and 'value' are required to POST.
        if 'name' in dir(self) and 'value' in dir(self):
            return True
        else:
            return False
