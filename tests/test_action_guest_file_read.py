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
from guest_file_read import InitiateFileTransferFromGuest

__all__ = [
    'InitiateFileTransferFromGuestTestCase'
]


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def raise_for_status(self):
            pass

    return MockResponse("mocktext", 200)


class InitiateFileTransferFromGuestTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = InitiateFileTransferFromGuest

    def test_normal(self):
        # test with and without guest_directory:
        for vars in [(None, '/tmp/foo.txt'), ('/tmp', 'foo.txt')]:
            (action, mock_vm) = self.mock_one_vm('vm-12345')
            mockFileMgr = mock.Mock()
            mockFileMgr.InitiateFileTransferFromGuest = mock.Mock()
            action.si_content.guestOperationsManager = mock.Mock()
            action.si_content.guestOperationsManager.fileManager = mockFileMgr
            with mock.patch('requests.get', side_effect=mocked_requests_get):
                result = action.run(vm_id='vm-12345',
                                    username='u',
                                    password='p',
                                    guest_directory=vars[0],
                                    guest_file=vars[1])
                mockFileMgr.InitiateFileTransferFromGuest.\
                    assert_called_once_with(
                        mock.ANY, mock.ANY, guestFilePath='/tmp/foo.txt')
                self.assertEqual(result, "mocktext")
