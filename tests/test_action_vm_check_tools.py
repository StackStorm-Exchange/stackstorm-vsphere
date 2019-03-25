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
from vm_check_tools import VMCheckTools
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'VMCheckTools'
]


class VMCheckToolsTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMCheckTools

    def setUp(self):
        super(VMCheckToolsTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch("vm_check_tools.json")
    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    def test_run(self, mock_get_virtualmachine, mock_json):
        test_vm_id = "test_vm"
        test_dict = {
            'test_option': 'value',
            'test_option_2': 'value_2',
            'test_option_3': 'value_3'
        }
        test_status = 'running'

        expected_result = test_dict
        expected_result['status'] = test_status

        mock_json.loads.return_value = test_dict
        mock_runtime = mock.Mock(powerState='poweredOn')
        mock_guest = mock.Mock(toolsRunningStatus='guestToolsRunning',
                              toolsVersionStatus2='installed')
        mock_vm = mock.Mock()
        mock_vm.runtime.return_value = mock_runtime
        mock_vm.guest.return_value = mock_guest

        mock_get_virtualmachine.return_value = mock_vm

        result_value = self._action.run(test_vm_id)
        self.assertEqual(result_value, expected_result)

    @mock.patch("vm_check_tools.json")
    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    def test_run_powered_off(self, mock_get_virtualmachine, mock_json):
        test_vm_id = "test_vm"
        test_dict = {
            'test_option': 'value',
            'test_option_2': 'value_2',
            'test_option_3': 'value_3'
        }

        expected_result = test_dict
        expected_result['status'] = 'poweredOff'

        mock_json.loads.return_value = test_dict
        mock_runtime = mock.Mock(powerState='poweredOff')
        mock_guest = mock.Mock(toolsRunningStatus='guestToolsRunning',
                              toolsVersionStatus2='installed')
        mock_vm = mock.Mock()
        mock_vm.runtime.return_value = mock_runtime
        mock_vm.guest.return_value = mock_guest

        mock_get_virtualmachine.return_value = mock_vm

        result_value = self._action.run(test_vm_id)
        self.assertEqual(result_value, expected_result)

    @mock.patch("vm_check_tools.json")
    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    def test_run_tools_not_installed(self, mock_get_virtualmachine, mock_json):
        test_vm_id = "test_vm"
        test_dict = {
            'test_option': 'value',
            'test_option_2': 'value_2',
            'test_option_3': 'value_3'
        }

        expected_result = test_dict
        expected_result['status'] = 'guestToolsNotInstalled'

        mock_json.loads.return_value = test_dict
        mock_runtime = mock.Mock(powerState='poweredOn')
        mock_guest = mock.Mock(toolsVersionStatus2='guestToolsNotInstalled')
        mock_vm = mock.Mock()
        mock_vm.runtime.return_value = mock_runtime
        mock_vm.guest.return_value = mock_guest

        mock_get_virtualmachine.return_value = mock_vm

        result_value = self._action.run(test_vm_id)
        self.assertEqual(result_value, expected_result)
