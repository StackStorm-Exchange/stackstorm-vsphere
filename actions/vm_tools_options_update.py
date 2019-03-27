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

from vmwarelib.actions import BaseAction
from vmwarelib import inventory


class VMToolsOptionsUpdate(BaseAction):
    def run(self, vm_id=None, vm_name=None, script_after_power_on=None, script_after_resume=None,
            script_before_guest_standby=None, script_before_guest_shutdown=None,
            script_before_guest_reboot=None, tools_upgrade_policy=None,
            sync_time_with_host=None, vsphere=None):

        if not vm_id and not vm_name:
            raise ValueError("Ether a VM Name or VM ID must be specified.")

        self.establish_connection(vsphere)

        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id, name=vm_name)

        spec = vim.vm.ConfigSpec()
        spec.tools = vim.vm.ToolsConfigInfo()

        # If any of the options are set to None then the value will not be changed.
        spec.tools.afterPowerOn = script_after_power_on
        spec.tools.afterResume = script_after_resume
        spec.tools.beforeGuestStandby = script_before_guest_standby
        spec.tools.beforeGuestShutdown = script_before_guest_shutdown
        spec.tools.beforeGuestReboot = script_before_guest_reboot
        spec.tools.toolsUpgradePolicy = tools_upgrade_policy
        spec.tools.syncTimeWithHost = sync_time_with_host

        task = vm.ReconfigVM_Task(spec)

        task_return = self._wait_for_task(task)

        return task_return
