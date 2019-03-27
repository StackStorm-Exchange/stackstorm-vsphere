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

from tag_category_delete import CategoryDelete
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'CategoryDeleteTestCase'
]


class CategoryDeleteTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = CategoryDelete

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "name"
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "vsphere": vsphere
        }
        test_category_id = "123"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = {'id': test_category_id}

        expected_result = "result"
        action.tagging.category_delete.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_find_by_name.assert_called_with(category_name)
        action.tagging.category_delete.assert_called_with(test_category_id)
        mock_connect.assert_called_with(vsphere)

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_fail(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "name"
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "vsphere": vsphere
        }

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = None

        expected_result = (False, "Category: 'name' not found!")

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_find_by_name.assert_called_with(category_name)
        mock_connect.assert_called_with(vsphere)
