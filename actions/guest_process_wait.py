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

from vmwarelib.guest import GuestAction
import eventlet  # pylint: disable=import-error
import sys


class WaitForProgramInGuest(GuestAction):

    def run(self, vm_id, username, password, pid, vsphere=None):
        """
        Wait for a program to exit in the guest.

        Args:
        - vm_id: MOID of the Virtual Machine
        - username: username to perform the operation
        - password: password of that user
        - pid: process id
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        """
        self.prepare_guest_operation(vsphere, vm_id, username, password)
        delay = 1
        max_delay = 8
        while True:
            inf = self.guest_process_manager.ListProcessesInGuest(
                vm=self.vm, auth=self.guest_credentials, pids=[pid])
            if not inf:
                raise Exception("No such process: " + str(pid))
            elif inf[0].endTime is not None:
                print(inf[0])
                sys.exit(inf[0].exitCode)
            else:
                eventlet.sleep(delay)
                delay = min(delay * 2, max_delay)
