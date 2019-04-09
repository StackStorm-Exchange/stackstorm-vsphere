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

from tag_category_create import CategoryCreate
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'CategoryCreateTestCase'
]


class CategoryCreateTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = CategoryCreate

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # mock
        expected_result = "result"
        action.tagging = mock.Mock()
        action.tagging.category_create.return_value = expected_result

        # define test variables
        category_name = "name"
        category_description = "test description"
        category_cardinality = "SINGLE"
        category_types = []
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "category_description": category_description,
            "category_cardinality": category_cardinality,
            "category_types": category_types,
            "vsphere": vsphere
        }

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_create.assert_called_with(category_name,
                                                          category_description,
                                                          category_cardinality,
                                                          category_types)
        mock_connect.assert_called_with(vsphere)
