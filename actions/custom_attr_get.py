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
from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class CustomAttrGet(BaseAction):
    def run(self, custom_attr_name, object_id, object_type, vsphere=None):
        """
        Get the value of a given Custom Attribute on an object

        Args:
        - custom_attr_name: name of custom attribute to get the value of
        - object_id: MOID of an object with a given custom attribute
        - object_type: vimType of convert object
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: string with value of the given custom attribute name
        """
        vimtype = self.get_vim_type(object_type)

        self.establish_connection(vsphere)

        # consult vSphere for the managed_entity object that is the specified ID and type
        entity = inventory.get_managed_entity(self.si_content, vimtype, moid=object_id)

        cfm = self.si_content.customFieldsManager

        # Find the ID of the custom attribute from the given name
        attr_id = next((field.key for field in cfm.field if field.name == custom_attr_name), None)

        if not attr_id:
            return(False, "Attribute: '%s' has no value on object: '%s'" %
                   (custom_attr_name, object_id))

        # Use the ID from above to find the value of the custom attribute on the object
        attr_value = next((attr.value for attr in entity.summary.customValue if
                           attr.key == attr_id), None)

        return (True, attr_value)
