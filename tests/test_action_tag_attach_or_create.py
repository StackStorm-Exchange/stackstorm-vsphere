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

from tag_attach_or_create import TagAttach
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TagAttachTestCase'
]


class TagAttachTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TagAttach

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_replace(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "cat_name"
        category_description = "Test Description"
        category_cardinality = "SINGLE"
        category_types = []
        tag_name = "tag_name"
        tag_description = "Test Description"
        object_type = "VirtualMachine"
        object_id = "vm-123"
        replace = True
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "category_description": category_description,
            "category_cardinality": category_cardinality,
            "category_types": category_types,
            "tag_name": tag_name,
            "tag_description": tag_description,
            "object_type": object_type,
            "object_id": object_id,
            "replace": replace,
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

        action.tagging.tag_association_replace.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_get_or_create.assert_called_with(category_name,
                                                                 category_description,
                                                                 category_cardinality,
                                                                 category_types)
        action.tagging.tag_get_or_create.assert_called_with(tag_name,
                                                            test_category_id,
                                                            tag_description)
        action.tagging.tag_association_replace.assert_called_with(test_tag_id,
                                                                  object_type,
                                                                  object_id)
        mock_connect.assert_called_with(vsphere)

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run_fail(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        category_name = "cat_name"
        category_description = "Test Description"
        category_cardinality = "SINGLE"
        category_types = []
        tag_name = "tag_name"
        tag_description = "Test Description"
        object_type = "VirtualMachine"
        object_id = "vm-123"
        replace = False
        vsphere = "default"
        test_kwargs = {
            "category_name": category_name,
            "category_description": category_description,
            "category_cardinality": category_cardinality,
            "category_types": category_types,
            "tag_name": tag_name,
            "tag_description": tag_description,
            "object_type": object_type,
            "object_id": object_id,
            "replace": replace,
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

        action.tagging.tag_association_attach.return_value = expected_result

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.category_get_or_create.assert_called_with(category_name,
                                                                 category_description,
                                                                 category_cardinality,
                                                                 category_types)
        action.tagging.tag_get_or_create.assert_called_with(tag_name,
                                                            test_category_id,
                                                            tag_description)
        action.tagging.tag_association_attach.assert_called_with(test_tag_id,
                                                                 object_type,
                                                                 object_id)
        mock_connect.assert_called_with(vsphere)
