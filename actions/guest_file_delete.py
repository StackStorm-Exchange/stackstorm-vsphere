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


class DeleteFileInGuest(GuestAction):

    def run(self, vm_id, username, password, guest_directory, guest_file,
            vsphere=None):
        """
        Delete a file inside a guest.

        Args:
        - vm_id: MOID of the Virtual Machine
        - username: username to perform the operation
        - password: password of that user
        - guest_directory: [optional] Directory in guest containing the file.
        - guest_file: Full path to file in guest to delete if guest_directory
        -             is not specified, otherwise this is relative.
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        """
        self.prepare_guest_operation(vsphere, vm_id, username, password)
        if not guest_directory:
            full_path = guest_file
        else:
            full_path = self.joinpath(guest_directory, guest_file)
        self.guest_file_manager.DeleteFileInGuest(
            self.vm, self.guest_credentials, full_path)
