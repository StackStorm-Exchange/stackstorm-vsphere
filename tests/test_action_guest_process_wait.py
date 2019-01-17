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
from guest_process_wait import WaitForProgramInGuest

__all__ = [
    'WaitForProgramInGuestTestCase'
]


class WaitForProgramInGuestTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = WaitForProgramInGuest

    def test_no_such_process(self):
        (action, mock_vm) = self.mock_one_vm('vm-12345')
        mockProcMgr = mock.Mock()
        mockProcMgr.ListProcessesInGuest = mock.Mock()
        mockProcMgr.ListProcessesInGuest.return_value = None
        action.si_content.guestOperationsManager = mock.Mock()
        action.si_content.guestOperationsManager.processManager = mockProcMgr
        with self.assertRaises(Exception):
            action.run(vm_id='vm-12345', username='u', password='p',
                       pid=12345)

    @mock.patch('eventlet.sleep')
    def test_wait_normal(self, mock_sleep):
        (action, mock_vm) = self.mock_one_vm('vm-12345')
        mockProcMgr = mock.Mock()
        mockProcMgr.ListProcessesInGuest = mock.Mock()
        still_running = mock.Mock()
        still_running.endTime = None
        finished = mock.Mock()
        finished.endTime = "yes"
        finished.exitCode = 42
        mockProcMgr.ListProcessesInGuest.side_effect =\
            [[still_running], [still_running], [still_running],
             [still_running], [still_running], [finished]]
        action.si_content.guestOperationsManager = mock.Mock()
        action.si_content.guestOperationsManager.processManager = mockProcMgr
        with self.assertRaises(SystemExit) as cm:
            action.run(vm_id='vm-12345', username='u', password='p',
                       pid=12345)
        self.assertEqual(cm.exception.code, 42)
