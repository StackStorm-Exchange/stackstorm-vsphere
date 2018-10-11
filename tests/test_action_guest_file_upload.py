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

import mock
from vsphere_base_action_test_case import VsphereBaseActionTestCase
from guest_file_upload import InitiateFileTransferToGuest

__all__ = [
    'InitiateFileTransferToGuestTestCase'
]


class InitiateFileTransferToGuestTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = InitiateFileTransferToGuest

    @mock.patch('__builtin__.open',
                mock.mock_open(read_data="mockfilecontents"))
    @mock.patch('requests.put')
    def test_normal(self, mock_put):
        # Exercise guest directory, one Windows, one Linux
        # guest_path[0] is the input guest_directory
        # guest_path[1] is the expected result
        for guest_path in (["C:\\WINDOWS\\TEMP", "C:\\WINDOWS\\TEMP\\myfile"],
                           ["/tmp", "/tmp/myfile"]):
            # Exercise both local_path variants
            for local_path in (
                '/opt/stackstorm/packs.dev/mypack/myfile',
                'pack:mypack/myfile'
            ):
                (action, mock_vm) = self.mock_one_vm('vm-12345')
                mockFileMgr = mock.Mock()
                mockFileMgr.InitiateFileTransferToGuest = mock.Mock()
                action.si_content.guestOperationsManager = mock.Mock()
                action.si_content.guestOperationsManager.fileManager =\
                    mockFileMgr
                result = action.run(vm_id='vm-12345',
                                    username='u',
                                    password='p',
                                    guest_directory=guest_path[0],
                                    local_path=local_path)
                mockFileMgr.InitiateFileTransferToGuest.assert_called_once()
                self.assertEqual(result, guest_path[1])
