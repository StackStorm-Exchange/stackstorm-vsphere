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

from custom_attr_create import CustomAttrCreate
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'CustomAttrCreateTestCase'
]


class CustomAttrCreateTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = CustomAttrCreate

    @mock.patch("vmwarelib.actions.BaseAction.establish_connection")
    def test_run(self, mock_connect):
        action = self.get_action_instance(self.new_config)

        # mock
        expected_result = "result"
        action.si_content = mock.Mock()
        action.si_content.customFieldsManager.AddCustomFieldDef.return_value = expected_result

        # define test variables
        custom_attr_name = "name"
        vsphere = "default"

        # invoke action with valid parameters
        result = action.run(custom_attr_name, vsphere)

        self.assertEqual(result, expected_result)
        action.si_content.customFieldsManager.AddCustomFieldDef.assert_called_with(
            name=custom_attr_name)
        mock_connect.assert_called_with(vsphere)
