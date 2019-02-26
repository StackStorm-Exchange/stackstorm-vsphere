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
from vm_folder_get import GetVMFolder


__all__ = [
    'GetVMFolderTestCase'
]


class GetVMFolderTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetVMFolder

    @mock.patch('vm_folder_get.inventory')
    def test_run(self, mock_inventory):
        test_vm_id = None
        test_vm_name = "test_vm_name"
        test_vsphere = "connection_details"

        action = self.get_action_instance(self.new_config)
        action.establish_connection = mock.Mock()
        action.si_content = "test_si_content"

        # Mock the datacenter object
        mock_dc = mock.MagicMock()
        mock_dc.name = "dctr1"
        mock_dc._wsdlName = "Datacenter"
        # Mock the VM folder
        mock_vm_folder = mock.MagicMock()
        mock_vm_folder.name = "vm"
        mock_vm_folder._wsdlName = "Folder"
        mock_vm_folder.parent = mock_dc
        # Mock the first parent folder object
        mock_parent = mock.MagicMock()
        mock_parent.name = "folder_name"
        mock_parent._wsdlName = "Folder"
        mock_parent.parent = mock_vm_folder
        # Mock the VM object
        mock_vm = mock.MagicMock()
        mock_vm.parent = mock_parent
        mock_inventory.get_virtualmachine.return_value = mock_vm

        # Output should be the full folder path to the VM, including the datacenter name
        expected_result = "/dctr1/vm/folder_name"

        # Execute the run function
        result = action.run(test_vm_id, test_vm_name, test_vsphere)

        # Verify the results
        self.assertEqual(result, expected_result)
        action.establish_connection.assert_called_with(test_vsphere)
        mock_inventory.get_virtualmachine.assert_called_with("test_si_content",
                                                             moid=test_vm_id,
                                                             name=test_vm_name)

    def test_run_blank_inputs(self):
        action = self.get_action_instance(self.new_config)
        self.assertRaises(ValueError, action.run, vm_id=None,
                          vm_name=None, vsphere="default")
