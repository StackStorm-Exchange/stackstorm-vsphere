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

import eventlet
from pyVmomi import vim  # pylint: disable-msg=E0611

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMApplyPowerState(BaseAction):

    def run(self, vm_id, vm_name, power_onoff, vsphere=None):
        """
        Set power state of targetted virtual machine

        Args:
        - vm_id: Moid of Virtual Machine to edit
        - vm_name: Name of Virtual Machine to edit
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        - power_onoff: Desired powerstate.

        Returns:
        - dict: State true/false
        """
        # check I have information to find a VM
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")

        self.establish_connection(vsphere)

        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id, name=vm_name)
        if not vm:
            raise Exception('Error: Unable to find VM')
        if power_onoff == "poweroff":
            task = vm.PowerOffVM_Task()
        elif power_onoff == "poweron":
            task = vm.PowerOnVM_Task()
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        return {'state': str(task.info.state)}
