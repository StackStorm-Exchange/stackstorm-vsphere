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
import requests


class InitiateFileTransferFromGuest(GuestAction):

    def run(self, vm_id, username, password, guest_directory, guest_file,
            vsphere=None):
        """
        Read the contents of a file on the guest.

        Args:
        - vm_id: MOID of the Virtual Machine
        - username: username to perform the operation
        - password: password of that user
        - guest_directory: full path to the directory containing the file
        - guest_file: full path to the file on the guest if guest_directory
        -             is None, otherwise a path relative to guest_directory
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        """
        self.prepare_guest_operation(vsphere, vm_id, username, password)
        if not guest_directory:
            full_path = guest_file
        else:
            full_path = self.joinpath(guest_directory, guest_file)
        dl_url = self.guest_file_manager.InitiateFileTransferFromGuest(
            self.vm, self.guest_credentials, guestFilePath=full_path)
        response = requests.get(dl_url.url, verify=False)
        response.raise_for_status()  # raise if status_code not 200
        return response.text
