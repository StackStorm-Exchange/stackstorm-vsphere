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
# limitations under the License.

import mock

# from vmwarelib import inventory
from host_get import GetHost
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetHost'
]


class GetHostTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetHost

    def setUp(self):
        super(GetHostTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_select_hosts(self):
        host_1 = mock.Mock()
        host_1_name_property = mock.PropertyMock(return_value='test_host')
        type(host_1).name = host_1_name_property
        host_1.summary = 'expected_summary'
        host_1._moId = 1

        host_2 = mock.Mock()
        host_2_name_property = mock.PropertyMock(return_value='test_host_2')
        type(host_2).name = host_2_name_property
        host_2.summary = 'expected_summary_2'
        host_2._moId = 2

        host_3 = mock.Mock()
        host_3_name_property = mock.PropertyMock(return_value='test_host_3')
        type(host_3).name = host_3_name_property
        host_3.summary = 'expected_summary_3'
        host_3._moId = 3

        host_4 = mock.Mock()
        host_4_name_property = mock.PropertyMock(return_value='test_host_4')
        type(host_4).name = host_4_name_property
        host_4.summary = 'expected_summary_4'
        host_4._moId = 4

        host_5 = mock.Mock()
        host_5_name_property = mock.PropertyMock(return_value='test_host_5')
        type(host_5).name = host_5_name_property
        host_5.summary = 'expected_summary_5'
        host_5._moId = 5

        mock_view = mock.Mock(view=[host_1, host_2, host_3, host_4, host_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = {
            'test_host_4': 'expected_summary_4',
            'test_host_2': 'expected_summary_2',
            'test_host_5': 'expected_summary_5'
        }

        result = self._action.get_select_hosts([4], ['test_host_2', 'test_host_5'])
        self.assertEqual(result, expected_result)

    def test_get_all_hosts(self):
        host_1 = mock.Mock()
        host_1_name_property = mock.PropertyMock(return_value='test_host')
        type(host_1).name = host_1_name_property
        host_1.summary = 'expected_summary'

        host_2 = mock.Mock()
        host_2_name_property = mock.PropertyMock(return_value='test_host_2')
        type(host_2).name = host_2_name_property
        host_2.summary = 'expected_summary_2'

        mock_view = mock.Mock(view=[host_1, host_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = {
            'test_host': 'expected_summary',
            'test_host_2': 'expected_summary_2'
        }

        result = self._action.get_all_hosts()
        self.assertEqual(result, expected_result)

    def test_run_select(self):
        host_1 = mock.Mock()
        host_1_name_property = mock.PropertyMock(return_value='test_host')
        type(host_1).name = host_1_name_property
        host_1.summary = 'expected_summary'
        host_1._moId = 1

        host_2 = mock.Mock()
        host_2_name_property = mock.PropertyMock(return_value='test_host_2')
        type(host_2).name = host_2_name_property
        host_2.summary = 'expected_summary_2'
        host_2._moId = 2

        host_3 = mock.Mock()
        host_3_name_property = mock.PropertyMock(return_value='test_host_3')
        type(host_3).name = host_3_name_property
        host_3.summary = 'expected_summary_3'
        host_3._moId = 3

        host_4 = mock.Mock()
        host_4_name_property = mock.PropertyMock(return_value='test_host_4')
        type(host_4).name = host_4_name_property
        host_4.summary = 'expected_summary_4'
        host_4._moId = 4

        host_5 = mock.Mock()
        host_5_name_property = mock.PropertyMock(return_value='test_host_5')
        type(host_5).name = host_5_name_property
        host_5.summary = 'expected_summary_5'
        host_5._moId = 5

        mock_view = mock.Mock(view=[host_1, host_2, host_3, host_4, host_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = {
            'test_host_4': 'expected_summary_4',
            'test_host_2': 'expected_summary_2',
            'test_host_5': 'expected_summary_5'
        }

        result = self._action.run([4], ['test_host_2', 'test_host_5'], False)
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        host_1 = mock.Mock()
        host_1_name_property = mock.PropertyMock(return_value='test_host')
        type(host_1).name = host_1_name_property
        host_1.summary = 'expected_summary'
        host_1._moId = 1

        host_2 = mock.Mock()
        host_2_name_property = mock.PropertyMock(return_value='test_host_2')
        type(host_2).name = host_2_name_property
        host_2.summary = 'expected_summary_2'
        host_2._moId = 2

        host_3 = mock.Mock()
        host_3_name_property = mock.PropertyMock(return_value='test_host_3')
        type(host_3).name = host_3_name_property
        host_3.summary = 'expected_summary_3'
        host_3._moId = 3

        host_4 = mock.Mock()
        host_4_name_property = mock.PropertyMock(return_value='test_host_4')
        type(host_4).name = host_4_name_property
        host_4.summary = 'expected_summary_4'
        host_4._moId = 4

        host_5 = mock.Mock()
        host_5_name_property = mock.PropertyMock(return_value='test_host_5')
        type(host_5).name = host_5_name_property
        host_5.summary = 'expected_summary_5'
        host_5._moId = 5

        mock_view = mock.Mock(view=[host_1, host_2, host_3, host_4, host_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = {
            'test_host': 'expected_summary',
            'test_host_2': 'expected_summary_2',
            'test_host_3': 'expected_summary_3',
            'test_host_4': 'expected_summary_4',
            'test_host_5': 'expected_summary_5'
        }

        result = self._action.run(None, None, True)
        self.assertEqual(result, expected_result)

    def test_run_error(self):
        # host_1 = mock.Mock()
        # host_1_name_property = mock.PropertyMock(return_value='test_host')
        # type(host_1).name = host_1_name_property
        # host_1.summary = 'expected_summary'
        # host_1._moId = 1

        # host_2 = mock.Mock()
        # host_2_name_property = mock.PropertyMock(return_value='test_host_2')
        # type(host_2).name = host_2_name_property
        # host_2.summary = 'expected_summary_2'
        # host_2._moId = 2

        # host_3 = mock.Mock()
        # host_3_name_property = mock.PropertyMock(return_value='test_host_3')
        # type(host_3).name = host_3_name_property
        # host_3.summary = 'expected_summary_3'
        # host_3._moId = 3

        # host_4 = mock.Mock()
        # host_4_name_property = mock.PropertyMock(return_value='test_host_4')
        # type(host_4).name = host_4_name_property
        # host_4.summary = 'expected_summary_4'
        # host_4._moId = 4

        # host_5 = mock.Mock()
        # host_5_name_property = mock.PropertyMock(return_value='test_host_5')
        # type(host_5).name = host_5_name_property
        # host_5.summary = 'expected_summary_5'
        # host_5._moId = 5

        # mock_view = mock.Mock(view=[host_1, host_2, host_3, host_4, host_5])
        # mock_vmware = mock.Mock(rootFolder="folder")
        # mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        # self._action.si_content = mock_vmware

        # expected_result = {
        #     'test_host': 'expected_summary',
        #     'test_host_2': 'expected_summary_2',
        #     'test_host_3': 'expected_summary_3',
        #     'test_host_4': 'expected_summary_4',
        #     'test_host_5': 'expected_summary_5'
        # }

        # result = self._action.run(False, None, None)
        # self.assertEqual(result, expected_result)

        self.assertRaises(ValueError, self._action.run, None, None, False)
