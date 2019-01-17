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
from guest_process_start import StartProgramInGuest

__all__ = [
    'StartProgramInGuestTestCase'
]


class StartProgramInGuestTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = StartProgramInGuest

    @mock.patch('pyVmomi.vim.vm.guest.ProcessManager')
    def test_normal(self, mock_process_manager):
        # Vary the arguments list including passing None
        # Each tuple has two array items, [0] is arguments input
        #                                 [1] is expected cmdspec
        for argdata in (None, 'onearg', 'two arguments'):
            (action, mock_vm) = self.mock_one_vm('vm-12345')
            mockProcMgr = mock.Mock()
            mockProcMgr.StartProgramInGuest = mock.Mock()
            mockProcMgr.StartProgramInGuest.return_value = 12345
            action.si_content.guestOperationsManager = mock.Mock()
            action.si_content.guestOperationsManager.processManager =\
                mockProcMgr
            mock_process_manager.ProgramSpec.return_value = 'cmdspec'

            envvars = ["A=B", "C=D"] if argdata else None
            result = action.run(vm_id='vm-12345', username='u',
                                password='p', command='c',
                                arguments=argdata, workdir='/tmp',
                                envvar=envvars)

            mock_process_manager.ProgramSpec.assert_called_with(
                arguments='' if not argdata else argdata,
                envVariables=envvars,
                programPath='c',
                workingDirectory='/tmp'
            )
            mockProcMgr.StartProgramInGuest.assert_called_once_with(
                mock_vm, action.guest_credentials, 'cmdspec',
            )

            self.assertEqual(result, 12345)
