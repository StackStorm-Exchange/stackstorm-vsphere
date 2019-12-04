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

from pyVmomi import vim  # pylint: disable-msg=E0611

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMRename(BaseAction):

    def run(self, new_name, vm_id, vsphere=None):
        """
        Remove virtual machine from vsphere

        Args:
        - vm_id: Moid of Virtual Machine to edit
        - new_name: Name to Virtual Machine to
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: success: true/false
        """

        self.establish_connection(vsphere)

        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)

        task = vm.Rename(new_name)
        success = self._wait_for_task(task)

        return {"success": success}
