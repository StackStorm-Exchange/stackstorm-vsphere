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
from vm_hw_scsi_controllers_get import VMSCSIControllersGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase
from vmwarelib.serialize import MyJSONEncoder
from pyVmomi import vim  # pylint: disable-msg=E0611

__all__ = [
    'VMSCSIControllersGet'
]


class VMSCSIControllersGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMSCSIControllersGet

    def setUp(self):
        super(VMSCSIControllersGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch("vm_hw_scsi_controllers_get.json")
    @mock.patch("vmwarelib.checkinputs.one_of_two_strings")
    @mock.patch("vmwarelib.inventory.get_virtualmachine")
    def test_run(self, mock_inventory, mock_check_inputs, mock_json):
        # Define test variables
        test_vm_id = "vm-123"
        test_vm_name = "test.vm.name"
        test_vsphere = "vsphere"

        test_controller1 = vim.vm.device.VirtualSCSIController()
        test_controller2 = vim.vm.device.VirtualSCSIController()
        device = [test_controller2, test_controller1]

        harware_mock = mock.Mock(device=device)
        config_mock = mock.Mock(hardware=harware_mock)
        vm_mock = mock.Mock(config=config_mock)
        mock_inventory.return_value = vm_mock

        json_string = "test json string"
        mock_json.dumps.return_value = json_string
        expected_result = "result"
        mock_json.loads.return_value = expected_result

        result = self._action.run(test_vm_id, test_vm_name, test_vsphere)

        self.assertEqual(result, expected_result)
        mock_check_inputs.assert_called_with(test_vm_id, test_vm_name, "ID or Name")
        mock_inventory.assert_called_with(self._action.si_content, test_vm_id, test_vm_name)
        self._action.establish_connection.assert_called_with(test_vsphere)
        mock_json.dumps.assert_called_with(device, cls=MyJSONEncoder)
        mock_json.loads.assert_called_with(json_string)
