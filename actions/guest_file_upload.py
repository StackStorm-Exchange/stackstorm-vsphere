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
from pyVmomi import vim  # pylint: disable-msg=E0611
import os
import requests


class InitiateFileTransferToGuest(GuestAction):

    def run(self, vm_id, username, password, guest_directory, local_path,
            vsphere=None):
        """
        Upload a file to a directory inside a guest.

        Args:
        - vm_id: MOID of the Virtual Machine
        - username: username to perform the operation
        - password: password of that user
        - guest_directory: Directory name in the guest to store the file
        - local_path: The full path to the local file, or a path
        -             relative to the packs directory when prefixed
        -             with pack:
        -             If this pack is a development pack (inside packs.dev)
        -             then the "pack:" prefix indicates packs.dev as the
        -             relative starting point.
        -             examples: /opt/stackstorm/packs/mypack/path/to/file
        -                       pack:mypack/path-inside-pack/to/file
        - vsphere: Pre-configured vsphere connection details (config.yaml)
        """
        self.prepare_guest_operation(vsphere, vm_id, username, password)

        if (local_path.startswith("pack:")):
            packsdir =\
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))))
            full_local_path = os.path.join(packsdir, local_path[5:])
        else:
            full_local_path = local_path

        with open(full_local_path, 'rb') as myfile:
            file_contents = myfile.read()
        guest_filename = os.path.basename(full_local_path)

        file_attribute = vim.vm.guest.FileManager.FileAttributes()
        full_path = self.joinpath(guest_directory, guest_filename)
        url = self.guest_file_manager.InitiateFileTransferToGuest(
            self.vm, self.guest_credentials, full_path, file_attribute,
            len(file_contents), True)

        response = requests.put(url, data=file_contents, verify=False)
        response.raise_for_status()  # raise if status_code is not 200
        return full_path
