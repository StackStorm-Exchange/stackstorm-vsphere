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


class GetTagValueFromObject(BaseAction):
    def run(self, **kwargs):
        """
        Connect to the REST API return a list of tag values for the given object and category

        Args:
        - kwargs: inputs to the aciton
          - category_name: Category of the tag to create
          - object_id: VMWare Object ID to get tags from (vm-1234)
          - object_type: Object type that corresponds to the ID (VirtualMachine)
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of tag values for the given object and category
        """
        self.connect_rest(kwargs.get("vsphere"))

        category = self.tagging.category_find_by_name(kwargs.get("category_name"))

        # Get a list of all tags on an object and compare that to a list of all tags from a
        # category then get the tag values from those ids
        if category:
            obj_tags = self.tagging.tag_association_list_attached_tags(kwargs.get("object_type"),
                                                                       kwargs.get("object_id"))
            cat_tags = self.tagging.tag_list(category['id'])
            tags = [self.tagging.tag_get(tag_id) for tag_id in cat_tags if tag_id in obj_tags]

            if tags:
                return [tag['name'] for tag in tags]
            else:
                return(False, "No tags found on object: '{}' with category: '{}'!".format(
                    kwargs.get("object_id"), kwargs.get("category_name")))
        else:
            return(False, "Category: '{}' not found!".format(kwargs.get("category_name")))
