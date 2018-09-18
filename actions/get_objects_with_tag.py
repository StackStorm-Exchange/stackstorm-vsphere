import requests
from vmwarelib.actions import BaseAction


class GetObjectsWithTag(BaseAction):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

    def get_objects_from_tag(self, kwargs_dict, session):
        """
        Make a REST API request that returns a list of all objects with a given tag

        Args:
        - kwargs_dict: Dictionary list of all inputs for this action
        - session: The session that's returned from the _connect_rest method

        Returns:
        - dict: The REST response from the API call
        """
        tag_id = kwargs_dict.get("tag_id")
        # Get the server from the vsphere config file
        if kwargs_dict.get("vsphere"):
            server = self.config['vsphere'].get(kwargs_dict.get("vsphere"))['host']
        else:
            server = self.config['vsphere'].get("default")['host']

        print("Test")
        print(server)

        tag_url = "https://%s/rest/com/vmware/cis/tagging/tag-association/id:%s?~action=" \
                  "list-attached-objects" % (server, tag_id)

        response = session.post(tag_url)
        response.raise_for_status()
        return response.json()

    def run(self, **kwargs):
        """
        Connect to the REST API and retrieve a list of objects with a given tag

        Args:
        - kwargs: inputs to the aciton

        Returns:
        - list: List of objects that are tagged with a given value
        """
        kwargs_dict = dict(kwargs)

        session = self._connect_rest(kwargs_dict.get("vsphere"))

        object_list = self.get_objects_from_tag(kwargs_dict, session)
        return object_list['value']
