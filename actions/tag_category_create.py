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


class CategoryCreate(BaseAction):
    def run(self, **kwargs):
        """
        Connect to the REST API and assign a list of tags to a given object

        Args:
        - kwargs: inputs to the aciton
          - category_cardinality: Cardinality of the tag category
          - category_description: Description of the tag category
          - category_name: Name of the tag category
          - category_types: Associable types for the tag category
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: Response from the category create POST request
        """
        self.connect_rest(kwargs.get("vsphere"))

        # create the category
        return self.tagging.category_create(kwargs.get("category_name"),
                                            kwargs.get("category_description"),
                                            kwargs.get("category_cardinality"),
                                            kwargs.get("category_types"))
