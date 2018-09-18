import requests
from vmwarelib.actions import BaseAction


class GetTagsOnObject(BaseAction):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

    def get_tag_list(self, kwargs_dict, session):
        """
        Make a REST API request that returns a list of all tags on a given object

        Args:
        - kwargs_dict: Dictionary list of all inputs for this action
        - session: The session that's returned from the _connect_rest method
                                                                                                                                               
        Returns:
        - dict: The REST response from the API call
        """
        if kwargs_dict.get("vsphere"):
            server = self.config['vsphere'].get(kwargs_dict.get("vsphere"))['host']
        else:
            server = self.config['vsphere'].get("default")['host']

        object_id = kwargs_dict.get("object_id")
        object_type = kwargs_dict.get("object_type")

        tag_url = "https://%s/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-tags" % server
        data = {
            "object_id": {
                "id": object_id,
                "type": object_type
            }
        }

        response = session.post(tag_url, json=data)
        response.raise_for_status()
        return response.json()

    def run(self, **kwargs):
        """
        Connect to the REST API and retrieve a list of tags on a given object

        Args:
        - kwargs: inputs to the aciton

        Returns:
        - list: List of tags that are on a given object
        """
        kwargs_dict = dict(kwargs)

        session = self._connect_rest(kwargs_dict.get("vsphere"))

        tag_list = self.get_tag_list(kwargs_dict, session)
        return tag_list['value']
