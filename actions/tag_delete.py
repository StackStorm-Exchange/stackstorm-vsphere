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


class TagDelete(BaseAction):
    def run(self, **kwargs):
        """
        Connect to the REST API and delete a tag from vSphere

        Args:
        - kwargs: inputs to the aciton
          - tag_category: Category of the tag to attach
          - tag_name: Name of the tag to attach
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: Response from the tag delete DELETE request
        """
        self.connect_rest(kwargs.get("vsphere"))

        category = self.tagging.category_find_by_name(kwargs.get("category_name"))

        if category:
            tag = self.tagging.tag_find_by_name(kwargs.get("tag_name"), category["id"])
            if tag:
                return self.tagging.tag_delete(tag["id"])
            else:
                return(False, "Tag: '{}' not found for category: "
                       "'{}'!".format(kwargs.get("tag_name"), kwargs.get("category_name")))
        else:
            return(False, "Category: '{}' not found!".format(kwargs.get("category_name")))
