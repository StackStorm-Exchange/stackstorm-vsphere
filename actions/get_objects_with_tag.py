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
        Connect to the REST API and retrieve a list of objects with a given tag id OR name

        Args:
        - kwargs: inputs to the aciton
          - category_name: Name of the tag category, only needed if tag name is given
          - tag_id: ID of the tag in VMWare
            (urn:vmomi:InventoryServiceTag:2f331011-d577-45a6-ab41-c6688de073f9:GLOBAL)
          - tag_name: name of the tag, not needed if tag id is given
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of objects that are tagged with a given value
        """
        self.connect_rest(kwargs.get("vsphere"))

        if kwargs.get("tag_id"):
            return self.tagging.tag_association_list_attached_objects(kwargs.get("tag_id"))
        elif kwargs.get("category_name") and kwargs.get("tag_name"):
            category = self.tagging.category_find_by_name(kwargs.get("category_name"))
            tag = self.tagging.tag_find_by_name(kwargs.get("tag_name"), category["id"])
            return self.tagging.tag_association_list_attached_objects(tag["id"])
        else:
            raise ValueError("Tag ID or Category name and Tag name are required!")
