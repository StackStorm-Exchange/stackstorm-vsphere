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

from vmwarelib import inventory
from get_moid import GetMoid
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetMoidTestCase'
]


class GetMoidTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetMoid

    def setUp(self):
        super(GetMoidTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_with_valid_name_and_type(self, mock_vim_type):
        # object types thats are assumed to be specified
        object_types = [
            'VirtualMachine',
            'Network',
            'Datastore',
            'Datacenter',
            'HostSystem',
        ]

        mock_vim_type.return_value = "vimType"

        # invoke action with valid parameters
        mock_entity = "''vim.VirtualMachine:vm-1234''"
        with mock.patch.object(inventory, 'get_managed_entity', return_value=mock_entity):
            # test for each object types
            for object_type in object_types:
                result = self._action.run(object_names=['hoge'], object_type=object_type)

                self.assertTrue(result[0])
                self.assertTrue(len(result[1]) > 0)
                self.assertEqual(result[1].get('hoge'), 'vm-1234')
                mock_vim_type.assert_called_with(object_type)

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_with_invalid_names(self, mock_vim_type):
        mock_vim_type.return_value = "vimType"

        def side_effect(*args, **kwargs):
            # because vmwarelib.inventory.get_managed_entity raises an exeption when
            # no matched object is found
            raise Exception("Inventory Error: Unable to Find Object in a test")

        # invoke action with invalid names which don't match any objects
        with mock.patch.object(inventory, 'get_managed_entity', side_effect=side_effect):
            with self.assertRaises(Exception):
                self._action.run(object_names=['hoge'], object_type='VirtualMachine')

        mock_vim_type.assert_called_with('VirtualMachine')
