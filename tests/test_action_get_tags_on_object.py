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

from get_tags_on_object import GetTagsOnObject
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetTagsOnObject'
]


class GetTagsOnObjectTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetTagsOnObject

    @mock.patch("vmwarelib.actions.BaseAction._rest_api_call")
    def test_run(self, mock_api_call):
        action = self.get_action_instance(self.new_config)

        # define test variables
        object_id = "123"
        object_type = "VM"
        vsphere = "default"
        test_kwargs = {
            "object_id": object_id,
            "object_type": object_type,
            "vsphere": vsphere
        }

        test_post_params = {
            "object_id": {
                "id": object_id,
                "type": object_type
            }
        }

        test_endpoint = "/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-tags"

        mock_api_call.return_value = {
            "value": "test"
        }

        # invoke action with valid parameters
        result = action.run(**test_kwargs)

        self.assertEqual(result, "test")
        mock_api_call.assert_called_with(vsphere, test_endpoint, "post", test_post_params)
