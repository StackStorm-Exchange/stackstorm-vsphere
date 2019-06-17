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
from vm_networks_get import GetVMNetworks


__all__ = [
    'GetVMNetworksTestCase'
]


class GetVMNetworksTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetVMNetworks

    @mock.patch('vmwarelib.checkinputs.one_of_two_strings')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run(self, mock_inventory, mock_check_inputs):
        action = self.get_action_instance(self.new_config)

        # Define test variables
        test_vm_id = "vm-123"
        test_vm_name = "test.vm.name"
        test_vsphere = "vsphere"
        test_si_content = "content"

        # Mock functions and results
        expected_result = ["net-name1", "net-name2"]
        action.si_content = test_si_content

        mock_network1 = mock.MagicMock()
        type(mock_network1).name = "net-name1"

        mock_network2 = mock.MagicMock()
        type(mock_network2).name = "net-name2"

        mock_get_vm = mock.MagicMock()
        mock_get_vm.network = [mock_network1, mock_network2]

        mock_inventory.return_value = mock_get_vm

        action.establish_connection = mock.MagicMock()
        mock_check_inputs.return_value = "check"

        result = action.run(test_vm_id, test_vm_name, test_vsphere)

        # Verify results
        self.assertEqual(result, expected_result)
        mock_check_inputs.assert_called_with(test_vm_id, test_vm_name, "ID or Name")
        mock_inventory.assert_called_with(test_si_content, moid=test_vm_id, name=test_vm_name)
        action.establish_connection.assert_called_with(test_vsphere)
