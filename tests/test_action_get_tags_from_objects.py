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

from get_tags_from_objects import GetTagsFromObjects
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetTagsFromObjectsTestCase'
]


class GetTagsFromObjectsTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetTagsFromObjects

    def test_get_tags(self):
        action = self.get_action_instance(self.new_config)

        # define test variables
        object_type = "VirtualMachine"
        object_id = "vm-123"

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.tag_association_list_attached_tags.return_value = ["345", "111", "987"]
        action.tagging.tag_get.side_effect = [
            {
                'tag_id': "987",
                'name': 'test_tag_1',
                'category_id': '123'
            }, {
                'tag_id': "012",
                'name': 'test_tag_2',
                'category_id': '456'
            }, {
                'tag_id': "385",
                'name': 'test_tag_3',
                'category_id': '678'
            }
        ]
        action.tagging.category_get.side_effect = [
            {
                'category_id': "123",
                'name': 'test_category_1',
            }, {
                'category_id': "456",
                'name': 'test_category_2',
            }, {
                'category_id': "678",
                'name': 'test_category_3',
            }
        ]

        expected_result = {
            'test_category_1': 'test_tag_1',
            'test_category_2': 'test_tag_2',
            'test_category_3': 'test_tag_3',
        }

        # invoke action with valid parameters
        result = action.get_tags(object_id, object_type)

        self.assertEqual(result, expected_result)
        action.tagging.tag_association_list_attached_tags.assert_called_with(
            object_type, object_id)

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # define test variables
        object_type = "VirtualMachine"
        object_ids = ["vm-123"]
        vsphere = "default"
        test_kwargs = {
            "object_type": object_type,
            "object_ids": object_ids,
            "vsphere": vsphere
        }

        # mock
        action.tagging = mock.MagicMock()
        action.tagging.tag_association_list_attached_tags.return_value = ["345", "111", "987"]
        action.tagging.tag_get.side_effect = [
            {
                'tag_id': "987",
                'name': 'test_tag_1',
                'category_id': '123'
            }, {
                'tag_id': "012",
                'name': 'test_tag_2',
                'category_id': '456'
            }, {
                'tag_id': "385",
                'name': 'test_tag_3',
                'category_id': '678'
            }
        ]
        action.tagging.category_get.side_effect = [
            {
                'category_id': "123",
                'name': 'test_category_1',
            }, {
                'category_id': "456",
                'name': 'test_category_2',
            }, {
                'category_id': "678",
                'name': 'test_category_3',
            }
        ]

        expected_result = {
            'vm-123': {
                'test_category_1': 'test_tag_1',
                'test_category_2': 'test_tag_2',
                'test_category_3': 'test_tag_3',
            }
        }

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)

        action.tagging.tag_association_list_attached_tags.assert_called_with(
            object_type, object_ids[0])

        mock_connect.assert_called_with(vsphere)
