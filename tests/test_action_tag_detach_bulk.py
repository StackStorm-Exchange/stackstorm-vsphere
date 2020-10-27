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

from tag_detach_bulk import TagDetachBulk
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TagDetachBulkTestCase'
]


class TagDetachBulkTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TagDetachBulk

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        bulk_object_type = "VirtualMachine"
        category_name = "cat_name"
        category_cardinality = "MULTIPLE"
        query_object_type = "VirtualMachine"
        query_object_name = "vm-123"
        tag_name = "tag_name"
        vsphere = "default"

        test_kwargs = {
            "bulk_object_type": bulk_object_type,
            "category_name": category_name,
            "category_cardinality": category_cardinality,
            "query_object_type": query_object_type,
            "query_object_name": query_object_name,
            "tag_name": tag_name,
            "vsphere": vsphere
        }
        test_category_id = "123"
        test_tag_id = "987"

        expected_result = "result"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_find_by_name.return_value = {'id': test_category_id}

        expected_result = "result"
        action.tagging.tag_find_by_name.return_value = {'id': test_tag_id}

        action.tagging.tag_bulk.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        mock_connect.assert_called_with(vsphere)
        action.tagging.category_find_by_name.assert_called_with(category_name)
        action.tagging.tag_find_by_name.assert_called_with(tag_name, "123")
        action.tagging.tag_bulk.assert_called_with(query_object_type=query_object_type,
                                                   query_object_name=query_object_name,
                                                   bulk_object_type=bulk_object_type,
                                                   category=category_name,
                                                   tag=tag_name,
                                                   cardinality=category_cardinality,
                                                   action='detach')
