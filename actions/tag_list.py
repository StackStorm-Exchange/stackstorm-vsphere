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


class TagList(BaseAction):
    def run(self, **kwargs):
        """
        List all tags from a given category or all tags if no category is given

        Args:
        - kwargs: inputs to the aciton
          - tag_category: Category to list tags from
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of all tags or tags from a given category
        """
        self.connect_rest(kwargs.get("vsphere"))

        # If a category is given, then verify that it exists
        # Otherwise return all tags from all categories
        category_id = None
        if kwargs.get("category_name"):
            category = self.tagging.category_find_by_name(kwargs.get("category_name"))
            if category:
                category_id = category["id"]
            else:
                return(False, "Category: '{}' not found!".format(kwargs.get("category_name")))

        return self.tagging.tag_list(category_id)
