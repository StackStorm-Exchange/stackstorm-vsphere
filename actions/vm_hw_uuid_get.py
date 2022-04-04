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


class GetVMUUID(BaseAction):

    def run(self, vm_ids, vm_names, vsphere=None):
        """
        Retrieve UUID for specified virtual machine.

        Args:
        - vm_id: Moid of Virtual Machine to edit
        - vm_name: Name of Virtual Machine to edit
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: uuid values.
        """
        results = []
        if not vm_ids and not vm_names:
            raise ValueError("No ID nor Names provided")

        self.establish_connection(vsphere)

        if vm_ids:
            for vm in vm_ids:
                vm = inventory.get_virtualmachine(self.si_content, moid=vm)
                if vm:
                    if vm.summary.config.uuid not in results:
                        results.append(vm.summary.config.uuid)
        if vm_names:
            for vm in vm_names:
                vm = inventory.get_virtualmachine(self.si_content, name=vm)
                if vm:
                    if vm.summary.config.uuid not in results:
                        results.append(vm.summary.config.uuid)
        return results
