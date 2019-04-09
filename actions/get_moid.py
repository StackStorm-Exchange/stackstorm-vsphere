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


class GetMoid(BaseAction):
    def run(self, object_names, object_type, vsphere=None):
        """
        Transform object_name and object_type to MOID (Managed Object Reference ID).

        Args:
        - object_name: name of object that is labeled to the target
        - object_type: vimType of convert object

        Returns:
        - dict: key value pair of object_name and moid.
        """
        vimtype = self.get_vim_type(object_type)

        self.establish_connection(vsphere)

        results = {}
        for name in object_names:
            try:
                # consult vSphere for the managed_entity object that is the specified name and type
                managed_entity = inventory.get_managed_entity(self.si_content, vimtype, name=name)

                # extract moid from vim.ManagedEntity object
                results[name] = str(managed_entity).split(':')[-1].replace("'", "")
            except Exception as e:
                self.logger.warning(str(e))

        return (True, results)
