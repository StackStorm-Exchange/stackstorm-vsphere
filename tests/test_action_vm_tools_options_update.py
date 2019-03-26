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

import mock

# from vmwarelib import inventory
from vm_tools_options_update import VMToolsOptionsUpdate
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'VMToolsOptionsUpdate'
]


class VMToolsOptionsUpdateCreateTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMToolsOptionsUpdate

    def setUp(self):
        super(VMToolsOptionsUpdateCreateTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    @mock.patch("vmwarelib.actions.BaseAction._wait_for_task")
    def test_run(self, mock__wait_for_task, mock_get_virtualmachine):
        test_dict = {
            'vm_name': 'test_name'
        }

        mock_vm = mock.Mock()
        mock_vm.ReconfigVM_Task.return_value = "vmWare Task"

        mock_get_virtualmachine.return_value = mock_vm
        mock__wait_for_task.return_value = True

        result_value = self._action.run(**test_dict)
        self.assertEqual(result_value, True)

    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    @mock.patch("vmwarelib.actions.BaseAction._wait_for_task")
    def test_run_options(self, mock__wait_for_task, mock_get_virtualmachine):
        test_dict = {
            'vm_id': 'test_id',
            'script_after_power_on': False,
            'script_after_resume': True,
            'script_before_guest_standby': False,
            'script_before_guest_shutdown': True,
            'script_before_guest_reboot': False,
            'tools_upgrade_policy': 'test',
            'sync_time_with_host': True,
        }

        mock_vm = mock.Mock()
        mock_vm.ReconfigVM_Task.return_value = "vmWare Task"

        mock_get_virtualmachine.return_value = mock_vm
        mock__wait_for_task.return_value = True

        result_value = self._action.run(**test_dict)
        self.assertEqual(result_value, True)

    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    @mock.patch("vmwarelib.actions.BaseAction._wait_for_task")
    def test_run_error(self, mock__wait_for_task, mock_get_virtualmachine):
        mock_vm = mock.Mock()
        mock_vm.ReconfigVM_Task.return_value = "vmWare Task"

        mock_get_virtualmachine.return_value = mock_vm
        mock__wait_for_task.return_value = True

        self.assertRaises(ValueError, self._action.run)
