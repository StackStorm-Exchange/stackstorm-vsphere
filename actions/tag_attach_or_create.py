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


class TagAttach(BaseAction):
    def run(self, **kwargs):
        """
        Attach a tag to a given object and create the tag and category if they don't exist

        Args:
        - kwargs: inputs to the aciton
          - category_cardinality: Cardinality of the tag category
          - category_description: Description of the tag category
          - category_name: Name of the tag category
          - category_types: Associable types for the tag category
          - object_id: VMWare Object ID to get tags from (vm-1234)
          - object_type: Object type that corresponds to the ID (VirtualMachine)
          - replace: Remove all tags with the given category before assigning the new one?
          - tag_description: Description of the tag to attach
          - tag_name: Name of the tag to attach
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: Response from the tag association POST request
        """
        self.connect_rest(kwargs.get("vsphere"))

        # create the category and tags
        category = self.tagging.category_get_or_create(kwargs.get("category_name"),
                                                       kwargs.get("category_description"),
                                                       kwargs.get("category_cardinality"),
                                                       kwargs.get("category_types"))

        tag = self.tagging.tag_get_or_create(kwargs.get("tag_name"), category["id"],
                                             kwargs.get("tag_description"))

        # If replace is selected, then all tags with the given category will be removed
        # from the VM before adding the new tag
        # This is needed when trying to change a tag with SINGLE cardinality
        if kwargs.get("replace"):
            return self.tagging.tag_association_replace(tag["id"], kwargs.get("object_type"),
                                                        kwargs.get("object_id"))
        else:
            return self.tagging.tag_association_attach(tag["id"], kwargs.get("object_type"),
                                                       kwargs.get("object_id"))
