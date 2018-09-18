# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vmwarelib.actions import BaseAction


class GetObjectsWithTag(BaseAction):
    def run(self, **kwargs):
        """
        Connect to the REST API and retrieve a list of objects with a given tag

        Args:
        - kwargs: inputs to the aciton
          - tag_id: ID og the tag in VMWare
            (urn:vmomi:InventoryServiceTag:2f331011-d577-45a6-ab41-c6688de073f9:GLOBAL)
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of objects that are tagged with a given value
        """
        kwargs_dict = dict(kwargs)

        api_endpoint = "/rest/com/vmware/cis/tagging/tag-association/id:%s?~action=" \
                       "list-attached-objects" % (kwargs_dict.get("tag_id"))

        object_list = self._rest_api_call(kwargs_dict.get("vsphere"), api_endpoint, "post")

        return object_list['value']
