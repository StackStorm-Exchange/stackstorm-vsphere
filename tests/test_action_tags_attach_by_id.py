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

from tags_attach_by_id import TagsAttachByID
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TagsAttachByID'
]


class TagsAttachToObjectTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TagsAttachByID

    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # mock
        expected_result = "result"
        action.tagging = mock.Mock()
        action.tagging.tag_association_attach_multiple.return_value = expected_result

        # define test variables
        object_id = "123"
        object_type = "VM"
        vsphere = "default"
        tag_ids = ["tag_id_1", "tag_id_2"]
        test_kwargs = {
            "object_id": object_id,
            "object_type": object_type,
            "vsphere": vsphere,
            "tag_ids": tag_ids
        }

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, expected_result)
        action.tagging.tag_association_attach_multiple.assert_called_with(tag_ids,
                                                                          object_type,
                                                                          object_id)
        mock_connect.assert_called_with(vsphere)
