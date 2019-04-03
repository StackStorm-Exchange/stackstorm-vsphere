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

from vmwarelib.actions import BaseAction
from vsphere_base_action_test_case import VsphereBaseActionTestCase
from get_objects_with_tag import GetObjectsWithTag

__all__ = [
    'BaseActionTestCase'
]


class BaseActionTestCase(VsphereBaseActionTestCase):
    __test__ = True
    # action_cls = BaseAction
    action_cls = GetObjectsWithTag

    def test_init(self):
        action = self.get_action_instance(self._new_config)
        self.assertIsInstance(action, BaseAction)

    def test_init_blank_config(self):
        with self.assertRaises(ValueError):
            self.get_action_instance(self._blank_config)

    def test_get_connection_info(self):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_vsphere = "default"
        # The following values are from the cfg_config_new
        expected_result = {'passwd': 'password', 'host': '192.168.0.1',
                           'port': 443, 'user': 'Admin'}

        # invoke action with a valid config
        result = action._get_connection_info(test_vsphere)

        self.assertEqual(result, expected_result)

    def test_get_connection_info_partial(self):
        action = self.get_action_instance(self._new_config_partial)

        # define test variables
        test_vsphere = "default"

        # invoke action with an invalid config
        with self.assertRaises(KeyError):
            action._get_connection_info(test_vsphere)

    @mock.patch("vmwarelib.actions.atexit.register")
    @mock.patch("vmwarelib.actions.connect.SmartConnect")
    def test_connect(self, mock_connect, mock_register):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_vsphere = "default"

        expected_result = "expected result"
        mock_connect.return_value = expected_result
        mock_register.return_value = "test"

        # invoke action with valid parameters
        result = action._connect(test_vsphere)

        self.assertEqual(result, expected_result)

    @mock.patch("vmwarelib.actions.requests.Session")
    def test_connect_rest(self, mock_session):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_vsphere = "default"
        test_endpoint = "https://%s/rest/com/vmware/cis/session" % \
                        self._new_config['vsphere']['default']['host']

        expected_result = mock.MagicMock()

        mock_session.return_value = expected_result

        # invoke action with valid parameters
        result = action.connect_rest(test_vsphere)

        self.assertEqual(result, expected_result)
        expected_result.post.assert_called_with(test_endpoint)

    @mock.patch("vmwarelib.actions.requests.Request")
    @mock.patch("vmwarelib.actions.BaseAction.connect_rest")
    def test_rest_api_call(self, mock_connect, mock_request):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_vsphere = "default"
        test_endpoint = "/api/test/endpoint"
        test_verb = "post"
        test_url = "https://%s/api/test/endpoint" % self._new_config['vsphere']['default']['host']

        expected_result = "expected result"
        mock_connect.return_value = mock.MagicMock()
        mock_connect.return_value.send.return_value.json.return_value = expected_result

        # invoke action with valid parameters
        result = action._rest_api_call(test_vsphere, test_endpoint, test_verb)

        self.assertEqual(result, expected_result)
        mock_request.assert_called_with(test_verb, test_url, json=None)
        mock_connect.assert_called_with(test_vsphere)

    @mock.patch("vmwarelib.actions.vim")
    def test_get_vim_type(self, mock_vim):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_object_type = "ObjectType"

        expected_result = mock.MagicMock()
        expected_result.return_value = "result"

        mock_vim.ObjectType = expected_result

        # invoke action with invalid object_type which is not registered in pyVmomi
        result = action.get_vim_type(test_object_type)

        self.assertEqual(result, expected_result)

    def test_get_vim_type_invalid(self):
        action = self.get_action_instance(self._new_config)

        # define test variables
        test_object_type = "InvalidObjectType"

        # invoke action with an invalid config
        with self.assertRaises(AttributeError):
            action.get_vim_type(test_object_type)
