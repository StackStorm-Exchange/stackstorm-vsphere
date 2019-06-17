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

from vsphere_base_action_test_case import VsphereBaseActionTestCase
from vm_config_info_get import GetVMConfigInfo
from vmwarelib.serialize import MyJSONEncoder
import mock


__all__ = [
    'GetVMConfigInfoTestCase'
]


class GetVMConfigInfoTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetVMConfigInfo

    def test_run_blank_input(self):
        action = self.get_action_instance(self.new_config)

        self.assertRaises(ValueError, action.run, vm_ids=None,
                          vm_names=None, vsphere="default")

    @mock.patch('vm_config_info_get.json')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run_vm_ids(self, mock_inventory, mock_json):
        action = self.get_action_instance(self.new_config)
        action.si_content = mock.Mock()
        action.establish_connection = mock.Mock()

        test_vm_ids = ["vm-100", "vm-101"]

        # Mock VM objects returned from inventory
        mock_vm1 = mock.MagicMock()
        type(mock_vm1).name = mock.PropertyMock(return_value="mock-vm1-name")
        mock_vm1.config = 'guest1'

        mock_vm2 = mock.MagicMock()
        type(mock_vm2).name = mock.PropertyMock(return_value="mock-vm2-name")
        mock_vm2.config = 'guest2'

        # Give return values to json functions
        mock_json.dumps.side_effect = ['dumps1', 'dumps2']
        mock_json.loads.side_effect = ['loads1', 'loads2']

        expected_result = {
            'mock-vm1-name': 'loads1',
            'mock-vm2-name': 'loads2'
        }

        mock_inventory.side_effect = [mock_vm1, mock_vm2]

        result = action.run(vm_ids=test_vm_ids, vm_names=None,
                            vsphere="vsphere")

        self.assertEqual(result, expected_result)

        mock_inventory.assert_has_calls([mock.call(action.si_content, moid="vm-100"),
                                         mock.call(action.si_content, moid="vm-101")])
        action.establish_connection.assert_called_with("vsphere")

        # The values from the following calls are from the side effects above
        mock_json.dumps.assert_has_calls([mock.call('guest1', cls=MyJSONEncoder),
                                          mock.call('guest2', cls=MyJSONEncoder)])
        mock_json.loads.assert_has_calls([mock.call('dumps1'),
                                          mock.call('dumps2')])

    @mock.patch('vm_config_info_get.json')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run_vm_names(self, mock_inventory, mock_json):
        action = self.get_action_instance(self.new_config)
        action.si_content = mock.Mock()
        action.establish_connection = mock.Mock()

        test_vm_names = ["mock-vm1-name", "mock-vm2-name"]

        # Mock VM objects returned from inventory
        mock_vm1 = mock.MagicMock()
        type(mock_vm1).name = mock.PropertyMock(return_value="mock-vm1-name")
        mock_vm1.config = 'guest1'

        mock_vm2 = mock.MagicMock()
        type(mock_vm2).name = mock.PropertyMock(return_value="mock-vm2-name")
        mock_vm2.config = 'guest2'

        # Give return values to json functions
        mock_json.dumps.side_effect = ['dumps1', 'dumps2']
        mock_json.loads.side_effect = ['loads1', 'loads2']

        expected_result = {
            'mock-vm1-name': 'loads1',
            'mock-vm2-name': 'loads2'
        }

        mock_inventory.side_effect = [mock_vm1, mock_vm2]

        result = action.run(vm_ids=None, vm_names=test_vm_names,
                            vsphere="vsphere")

        self.assertEqual(result, expected_result)

        mock_inventory.assert_has_calls([mock.call(action.si_content, name="mock-vm1-name"),
                                         mock.call(action.si_content, name="mock-vm2-name")])
        action.establish_connection.assert_called_with("vsphere")

        # The values from the following calls are from the side effects above
        mock_json.dumps.assert_has_calls([mock.call('guest1', cls=MyJSONEncoder),
                                          mock.call('guest2', cls=MyJSONEncoder)])
        mock_json.loads.assert_has_calls([mock.call('dumps1'),
                                          mock.call('dumps2')])
