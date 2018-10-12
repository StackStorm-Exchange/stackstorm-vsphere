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


class VMShutdownGuest(BaseAction):

    def run(self, id, vsphere=None):
        """
        Initiate a clean shutdown on one or more VMs.

        Args:
        - id: [array] MOIDs of Virtual Machines to shutdown.
        - vsphere: Pre-configured vSphere connection details (config.yaml)

        Returns:
        - task
        """

        self.establish_connection(vsphere)
        for vm_id in id:
            vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)
            return vm.ShutdownGuest()
