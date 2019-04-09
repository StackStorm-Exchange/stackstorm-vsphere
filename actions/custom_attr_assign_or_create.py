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


class CustomAttrAssignOrCreate(BaseAction):
    def run(self, custom_attr_name, custom_attr_value, object_id, object_type, vsphere=None):
        """
        Create a custom attribute if it doesn't exist and asssign it to a given object

        Args:
        - custom_attr_name: name of custom attribute to assign
        - custom_attr_value: value of custom attribute to assign
        - object_id: MOID of an object to assign a custom attribute to
        - object_type: vimType of convert object
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - string: string with success or error message
        """
        vimtype = self.get_vim_type(object_type)

        self.establish_connection(vsphere)

        # consult vSphere for the managed_entity object that is the specified name and type
        entity = inventory.get_managed_entity(self.si_content, vimtype, moid=object_id)

        cfm = self.si_content.customFieldsManager

        # Get the custom attribute object with the given name or 'None' if it isn't found
        field = next((field for field in cfm.field if field.name == custom_attr_name), None)

        if field is None:
            field = cfm.AddCustomFieldDef(name=custom_attr_name)

        cfm.SetField(entity=entity, key=field.key, value=custom_attr_value)

        return (True, "Attribute: '%s' set on object: '%s' with value: '%s'" %
                (custom_attr_name, object_id, custom_attr_value))
