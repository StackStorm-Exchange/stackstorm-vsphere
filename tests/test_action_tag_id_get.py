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

from tag_id_get import TagIdGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TagIdGetTestCase'
]


class TagIdGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TagIdGet

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # mock
        action.tagging = mock.Mock()

        test_cat_id = "123"
        test_category = {"id": test_cat_id}
        action.tagging.category_find_by_name.return_value = test_category

        test_tag_id = "789"
        test_tag = {"id": test_tag_id}
        action.tagging.tag_find_by_name.return_value = test_tag

        # define test variables
        category_name = "cat"
        tag_name = "tag"
        vsphere = "default"

        # invoke action with valid parameters
        result = action.run(category_name, tag_name, vsphere)

        self.assertEqual(result, test_tag_id)
        action.tagging.category_find_by_name.assert_called_with(category_name)
        action.tagging.tag_find_by_name.assert_called_with(tag_name, test_cat_id)
        mock_connect.assert_called_with(vsphere)
