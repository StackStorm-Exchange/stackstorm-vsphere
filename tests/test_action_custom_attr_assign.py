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
from custom_attr_assign import CustomAttrAssign
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'CustomAttrAssign'
]


class CustomAttrAssignTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = CustomAttrAssign

    def setUp(self):
        super(CustomAttrAssignTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_with_valid_inputs(self, mock_vim_type):
        # object types thats are assumed to be specified
        test_custom_attr_name = "Field 2"
        test_custom_attr_value = "test"
        test_object_id = "obj-123"
        test_object_type = "VirtualMachine"
        test_vim_type = "vimType"

        mock_vim_type.return_value = test_vim_type

        # Mock field objects with mocked key and name attributes
        mock_field_1 = mock.MagicMock(key='123')
        mock_field_2 = mock.MagicMock(key='321')
        type(mock_field_1).name = mock.PropertyMock(return_value='Field 1')
        type(mock_field_2).name = mock.PropertyMock(return_value='Field 2')
        test_fields = [mock_field_1, mock_field_2]

        self._action.si_content.customFieldsManager.field = test_fields

        # invoke action with valid parameters
        mock_entity = "''vim.VirtualMachine:vm-1234''"
        with mock.patch.object(inventory, 'get_managed_entity', return_value=mock_entity):
            result = self._action.run(test_custom_attr_name, test_custom_attr_value,
                                      test_object_id, test_object_type)

            self.assertTrue(result[0])
            self.assertEqual(result[1], "Attribute: '%s' set on object: '%s' with value: '%s'" %
                             (test_custom_attr_name, test_object_id, test_custom_attr_value))
            self._action.si_content.customFieldsManager.SetField.assert_called_with(
                entity=mock_entity, key='321', value=test_custom_attr_value)
            mock_vim_type.assert_called_with(test_object_type)

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_with_invalid_names(self, mock_vim_type):
        test_custom_attr_name = "Test Attr"
        test_custom_attr_value = "test"
        test_object_id = "obj-123"
        test_object_type = "VirtualMachine"
        test_vim_type = "vimType"

        mock_vim_type.return_value = test_vim_type

        def side_effect(*args, **kwargs):
            # because vmwarelib.inventory.get_managed_entity raises an exeption when
            # no matched object is found
            raise Exception("Inventory Error: Unable to Find Object in a test")

        # invoke action with invalid names which don't match any objects
        with self.assertRaises(Exception):
            with mock.patch.object(inventory, 'get_managed_entity', side_effect=side_effect):
                self._action.run(test_custom_attr_name, test_custom_attr_value,
                                 test_object_id, test_object_type)

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_with_invalid_attr(self, mock_vim_type):
        # object types thats are assumed to be specified
        test_custom_attr_name = "Invalid"
        test_custom_attr_value = "test"
        test_object_id = "obj-123"
        test_object_type = "VirtualMachine"
        test_vim_type = "vimType"

        mock_vim_type.return_value = test_vim_type

        # Mock field objects with mocked name attributes
        mock_field_1 = mock.MagicMock()
        mock_field_2 = mock.MagicMock()
        type(mock_field_1).name = mock.PropertyMock(return_value='Field 1')
        type(mock_field_2).name = mock.PropertyMock(return_value='Field 2')
        test_fields = [mock_field_1, mock_field_2]

        self._action.si_content.customFieldsManager.field = test_fields

        # invoke action with valid parameters
        mock_entity = "''vim.VirtualMachine:vm-1234''"
        with mock.patch.object(inventory, 'get_managed_entity', return_value=mock_entity):
            result = self._action.run(test_custom_attr_name, test_custom_attr_value,
                                      test_object_id, test_object_type)

            self.assertFalse(result[0])
            self.assertEqual(result[1], "Attribute: '%s' not found for object type: %s!" %
                             (test_custom_attr_name, test_object_type))
            mock_vim_type.assert_called_with(test_object_type)
