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

from get_tag_value_from_object import GetTagValueFromObject
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetTagValueFromObjectTestCase'
]


class GetTagValueFromObjectTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetTagValueFromObject

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "cat_name"
        tag_name = "tag_name"
        object_type = "VirtualMachine"
        object_id = "vm-123"
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "tag_name": tag_name,
            "object_type": object_type,
            "object_id": object_id,
            "vsphere": vsphere
        }
        test_category_id = "123"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = {'id': test_category_id}

        action.tagging.tag_association_list_attached_tags.return_value = ["345", "111", "987"]

        action.tagging.tag_list.return_value = ["987", "012", "385"]

        expected_result = "result"
        action.tagging.tag_get.return_value = {'name': expected_result}

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, [expected_result])
        action.tagging.category_find_by_name.assert_called_with(category_name)

        action.tagging.tag_association_list_attached_tags.assert_called_with(
            object_type, object_id)

        action.tagging.tag_list.assert_called_with(test_category_id)

        action.tagging.tag_get.assert_called_with("987")

        mock_connect.assert_called_with(vsphere)

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_category_not_found(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "cat_name"
        tag_name = "tag_name"
        object_type = "VirtualMachine"
        object_id = "vm-123"
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "tag_name": tag_name,
            "object_type": object_type,
            "object_id": object_id,
            "vsphere": vsphere
        }

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = None

        expected_result = (False, "Category: 'cat_name' not found!")

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_find_by_name.assert_called_with(category_name)
        mock_connect.assert_called_with(vsphere)

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_tag_not_found(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "cat_name"
        tag_name = "tag_name"
        object_type = "VirtualMachine"
        object_id = "vm-123"
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "tag_name": tag_name,
            "object_type": object_type,
            "object_id": object_id,
            "vsphere": vsphere
        }
        test_category_id = "123"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = {'id': test_category_id}

        action.tagging.tag_association_list_attached_tags.return_value = ["345", "111", "987"]

        action.tagging.tag_list.return_value = ["765", "012", "385"]

        expected_result = "result"
        action.tagging.tag_get.return_value = []

        expected_result = (False, "No tags found on object: 'vm-123' with category: 'cat_name'!")

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_find_by_name.assert_called_with(category_name)

        action.tagging.tag_association_list_attached_tags.assert_called_with(
            object_type, object_id)

        action.tagging.tag_list.assert_called_with(test_category_id)

        action.tagging.tag_get.assert_not_called()

        mock_connect.assert_called_with(vsphere)
