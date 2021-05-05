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


class GetTagsOnObject(BaseAction):
    def run(self, **kwargs):
        """
        Connect to the REST API and retrieve a list of tags on a given object

        Args:
        - kwargs: inputs to the aciton
          - object_id: VMWare Object ID to get tags from (vm-1234)
          - object_type: Object type that corresponds to the ID (VirtualMachine)
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of tags that are on a given object
        """
        self.connect_rest(kwargs.get("vsphere"))

        return self.tagging.tag_association_list_attached_tags(kwargs.get("object_type"),
                                                               kwargs.get("object_id"))
