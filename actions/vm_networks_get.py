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
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class GetVMNetworks(BaseAction):
    def run(self, vm_id, vm_name, vsphere=None):
        """
        Retrieve a list of network names that the given VM is on

        Args:
        - vm_id: Moid of Virtual Machine to retrieve
        - vm_name: Name of Virtual Machine to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: network names that the VM is connected to
        """

        # check a means of finding the VM has been provided
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")
        self.establish_connection(vsphere)

        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id,
                                          name=vm_name)

        # return a list of network names that the VM is on
        return map(lambda x: x.name, vm.network)
