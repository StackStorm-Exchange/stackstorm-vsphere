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

# import yaml
# from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_rename import VMRename
import mock


__all__ = [
    'VMRenameTestCase'
]


class VMRenameTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMRename

    @mock.patch('vm_rename.VMRename._wait_for_task')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run_vm_ids(self, mock_inventory, mock_wait_for_task):
        action = self.get_action_instance(self.new_config)
        action.si_content = mock.Mock()
        action.establish_connection = mock.Mock()

        test_vm_ids = "vm-100"

        # Mock VM objects returned from inventory
        mock_vm1 = mock.MagicMock()
        type(mock_vm1).name = mock.PropertyMock(return_value="mock-vm1-name")
        mock_vm1.Rename().return_value = 'task'

        mock_wait_for_task.return_value = True

        result = action.run(vm_id=test_vm_ids, new_name='test', vsphere="vsphere")

        self.assertEqual(result, {"success": True})
