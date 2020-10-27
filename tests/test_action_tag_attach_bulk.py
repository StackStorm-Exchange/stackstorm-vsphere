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

from tag_attach_bulk import TagAttachBulk
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TagAttachBulkTestCase'
]


class TagAttachBulkTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TagAttachBulk

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        bulk_object_type = "VirtualMachine"
        category_name = "cat_name"
        category_description = "Test Description"
        category_cardinality = "SINGLE"
        category_types = []
        query_object_type = "VirtualMachine"
        query_object_name = "vm-123"
        replace = False
        tag_name = "tag_name"
        tag_description = "Test Description"
        vsphere = "default"

        test_kwargs = {
            "bulk_object_type": bulk_object_type,
            "category_name": category_name,
            "category_description": category_description,
            "category_cardinality": category_cardinality,
            "category_types": category_types,
            "query_object_type": query_object_type,
            "query_object_name": query_object_name,
            "replace": replace,
            "tag_name": tag_name,
            "tag_description": tag_description,
            "vsphere": vsphere
        }
        test_category_id = "123"
        test_tag_id = "987"

        expected_result = "result"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_get_or_create.return_value = {'id': test_category_id}

        expected_result = "result"
        action.tagging.tag_get_or_create.return_value = {'id': test_tag_id}

        action.tagging.tag_bulk.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        mock_connect.assert_called_with(vsphere)
        action.tagging.category_get_or_create.assert_called_with(category_name,
                                                                 category_description,
                                                                 category_cardinality,
                                                                 category_types)
        action.tagging.tag_get_or_create.assert_called_with(tag_name,
                                                            test_category_id,
                                                            tag_description)
        action.tagging.tag_bulk.assert_called_with(query_object_type=query_object_type,
                                                   query_object_name=query_object_name,
                                                   bulk_object_type=bulk_object_type,
                                                   category=category_name,
                                                   tag=tag_name,
                                                   cardinality=category_cardinality,
                                                   action='add')

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_replace(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        bulk_object_type = "VirtualMachine"
        category_name = "cat_name"
        category_description = "Test Description"
        category_cardinality = "SINGLE"
        category_types = []
        query_object_type = "VirtualMachine"
        query_object_name = "vm-123"
        replace = True
        tag_name = "tag_name"
        tag_description = "Test Description"
        vsphere = "default"

        test_kwargs = {
            "bulk_object_type": bulk_object_type,
            "category_name": category_name,
            "category_description": category_description,
            "category_cardinality": category_cardinality,
            "category_types": category_types,
            "query_object_type": query_object_type,
            "query_object_name": query_object_name,
            "replace": replace,
            "tag_name": tag_name,
            "tag_description": tag_description,
            "vsphere": vsphere
        }
        test_category_id = "123"
        test_tag_id = "987"

        expected_result = "result"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.category_get_or_create.return_value = {'id': test_category_id}

        expected_result = "result"
        action.tagging.tag_get_or_create.return_value = {'id': test_tag_id}

        action.tagging.tag_bulk.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        mock_connect.assert_called_with(vsphere)
        action.tagging.category_get_or_create.assert_called_with(category_name,
                                                                 category_description,
                                                                 category_cardinality,
                                                                 category_types)
        action.tagging.tag_get_or_create.assert_called_with(tag_name,
                                                            test_category_id,
                                                            tag_description)
        action.tagging.tag_bulk.assert_called_with(query_object_type=query_object_type,
                                                   query_object_name=query_object_name,
                                                   bulk_object_type=bulk_object_type,
                                                   category=category_name,
                                                   tag=tag_name,
                                                   cardinality=category_cardinality,
                                                   action='replace')
