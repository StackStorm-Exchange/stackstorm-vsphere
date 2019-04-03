# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vmwarelib.actions import BaseAction


class CustomAttrCreate(BaseAction):
    def run(self, custom_attr_name, vsphere=None):
        """
        Create a custom attribute with the given name

        Args:
        - custom_attr_name: name of custom attribute to assign
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - object: newly created CustomFieldDef object
        """
        self.establish_connection(vsphere)

        cfm = self.si_content.customFieldsManager

        return cfm.AddCustomFieldDef(name=custom_attr_name)
