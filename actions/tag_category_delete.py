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


class CategoryDelete(BaseAction):
    def run(self, **kwargs):
        """
        Delete a tag category from vsphere

        Args:
        - kwargs: inputs to the aciton
          - category_name: Category name to delete
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: Response from the category delete DELETE request
        """
        self.connect_rest(kwargs.get("vsphere"))

        category = self.tagging.category_find_by_name(kwargs.get("category_name"))

        if category:
            return self.tagging.category_delete(category["id"])
        else:
            return(False, "Category: '{}' not found!".format(kwargs.get("category_name")))
