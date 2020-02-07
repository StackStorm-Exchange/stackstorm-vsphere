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

import os

from pyVmomi import vim  # pylint: disable-msg=E0611

from .actions import BaseAction
from .inventory import get_virtualmachine


class GuestAction(BaseAction):
    """
    GuestAction configures typical settings and properties to
    execute a Guest Operations command against a single VM.
    """
    def prepare_guest_operation(self, vsphere, vm_id, username, password):
        """
        Args:
        - vsphere: The pre-configured vSphere connection details.
        - vm_id: The MOID of the VM.
        - username: The username within the VM.
        - password: The password for that username.

        Configures Properties:
        - content
        - guest_credentials
        - guest_file_manager
        - guest_operations_manager
        - guest_process_manager
        - vm
        """
        self.establish_connection(vsphere)
        self._creds = self._auth_username_password(username=username,
                                                   password=password)
        self._vm = get_virtualmachine(self.content, moid=vm_id)

    @property
    def guest_credentials(self):
        return self._creds

    @property
    def guest_file_manager(self):
        return self.guest_operations_manager.fileManager

    @property
    def guest_operations_manager(self):
        return self.si_content.guestOperationsManager

    @property
    def guest_process_manager(self):
        return self.guest_operations_manager.processManager

    @property
    def vm(self):
        return self._vm

    def joinpath(self, path, nxt):
        """
        os.path.join makes assumptions based on the OS of the
        caller.  In this case we may be dealing with a path from
        a foreign OS.  If the path contains a colon followed
        by a backslash (NOTE: this is perfectly legal in POSIX)
        we assume it is for Windows.

        Args:
        - path: the left part of the path
        - nxt: the next element to append to the path

        Returns:
        - A full path
        """
        sep = "\\" if ":\\" in path else os.sep
        return path.rstrip(sep) + sep + nxt.strip(sep)

    def _auth_username_password(self, username=None, password=None):
        return vim.vm.guest.NamePasswordAuthentication(username=username,
                                                       password=password)
