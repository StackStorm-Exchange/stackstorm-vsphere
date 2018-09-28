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


class CreateTemporaryDirectoryInGuest(GuestAction):

    def run(self, vm_id, username, password, prefix, suffix, vsphere=None):
        """
        Create a temporary directory inside a guest.

        Args:
        - vm_id: MOID of the Virtual Machine
        - username: username to perform the operation
        - password: password of that user
        - prefix: Directory name prefix, recommend trailing with underscore
        - suffix: Directory name suffix; recommend leading with underscore
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - the new directory name (a full path known to the guest)

        Throws:
        - Exception when something goes wrong
          TODO: this should be improved
        """

        self.prepare_guest_operation(vsphere, vm_id, username, password)
        return self.guest_file_manager.CreateTemporaryDirectoryInGuest(
            self.vm, self.guest_credentials, prefix, suffix)
