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
from custom_attr_get import CustomAttrGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'CustomAttrGet'
]


class CustomAttrGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = CustomAttrGet

    def setUp(self):
        super(CustomAttrGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

        # Mock customFieldsManager.field objects with mocked key and name attributes
        mock_field_1 = mock.MagicMock(key='123')
        mock_field_2 = mock.MagicMock(key='321')
        type(mock_field_1).name = mock.PropertyMock(return_value='Field 1')
        type(mock_field_2).name = mock.PropertyMock(return_value='Field 2')
        test_fields = [mock_field_1, mock_field_2]

        self._action.si_content.customFieldsManager.field = test_fields

        # Mock summary.customValue objects with mocked key and value attributes
        mock_value_1 = mock.MagicMock(key='123', value='Value 1')
        mock_value_2 = mock.MagicMock(key='321', value='Value 2')
        test_values = [mock_value_1, mock_value_2]

        self._entity = mock.MagicMock()
        self._entity.summary.customValue = test_values

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_attribute_exists(self, mock_vim_type):
        test_custom_attr_name = "Field 2"
        test_object_id = "obj-123"
        test_object_type = "VirtualMachine"
        test_vim_type = "vimType"

        mock_vim_type.return_value = test_vim_type

        with mock.patch.object(inventory, 'get_managed_entity', return_value=self._entity):
            result = self._action.run(test_custom_attr_name, test_object_id, test_object_type)

            self.assertTrue(result[0])
            self.assertEqual(result[1], "Value 2")
            mock_vim_type.assert_called_with(test_object_type)

    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_attribute_not_exists(self, mock_vim_type):
        test_custom_attr_name = "Field 3"
        test_object_id = "obj-123"
        test_object_type = "VirtualMachine"
        test_vim_type = "vimType"

        mock_vim_type.return_value = test_vim_type

        with mock.patch.object(inventory, 'get_managed_entity', return_value=self._entity):
            result = self._action.run(test_custom_attr_name, test_object_id, test_object_type)

            self.assertFalse(result[0])
            self.assertEqual(result[1], "Attribute: '%s' has no value on object: '%s'" %
                             (test_custom_attr_name, test_object_id))
            mock_vim_type.assert_called_with(test_object_type)
