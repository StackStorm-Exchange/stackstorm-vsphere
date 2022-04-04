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
from pyVmomi import vim  # pylint: disable-msg=E0611

# from vmwarelib import inventory
from network_get import NetworkGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'NetworkGet'
]


class NetworkGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = NetworkGet

    def setUp(self):
        super(NetworkGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_network_dict(self):
        network_1 = mock.Mock()
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary
        network_1._moId = 1

        expected_result = {
            'name': 'test_network',
            'id': 1,
            'is_dvs': False,
            'summary': expected_sumary
        }

        result = self._action.get_network_dict(network_1)
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name(self):
        network_1 = mock.Mock()
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary_1 = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary_1
        network_1._moId = 1

        network_2 = mock.Mock()
        network_2_name_property = mock.PropertyMock(return_value='test_network_2')
        type(network_2).name = network_2_name_property
        expected_sumary_2 = {
            'network': {
                '_moId': 2
            }
        }
        network_2.summary = expected_sumary_2
        network_2._moId = 2

        network_3 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_3_name_property = mock.PropertyMock(return_value='test_network_3')
        type(network_3).name = network_3_name_property
        expected_sumary_3 = {
            'network': {
                '_moId': 3
            }
        }
        network_3.summary = expected_sumary_3
        network_3._moId = 3

        network_4 = mock.Mock()
        network_4_name_property = mock.PropertyMock(return_value='test_network_4')
        type(network_4).name = network_4_name_property
        expected_sumary_4 = {
            'network': {
                '_moId': 4
            }
        }
        network_4.summary = expected_sumary_4
        network_4._moId = 4

        network_5 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_5_name_property = mock.PropertyMock(return_value='test_network_5')
        type(network_5).name = network_5_name_property
        expected_sumary_5 = {
            'network': {
                '_moId': 5
            }
        }
        network_5.summary = expected_sumary_5
        network_5._moId = 5

        mock_view = mock.Mock(view=[network_1,
                                    network_2,
                                    network_3,
                                    network_4,
                                    network_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_network_4',
                'id': 4,
                'is_dvs': False,
                'summary': expected_sumary_4
            }, {
                'name': 'test_network_2',
                'id': 2,
                'is_dvs': False,
                'summary': expected_sumary_2
            }, {
                'name': 'test_network_5',
                'id': 5,
                'is_dvs': True,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.get_by_id_or_name([4], ['test_network_2', 'test_network_5'])
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name_duplicate(self):
        network_1 = mock.Mock()
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary_1 = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary_1
        network_1._moId = 1

        mock_view = mock.Mock(view=[network_1])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_network',
                'id': 1,
                'is_dvs': False,
                'summary': expected_sumary_1
            }
        ]

        result = self._action.get_by_id_or_name([1], ['test_network'])
        self.assertEqual(result, expected_result)

    def test_get_all_networks(self):
        network_1 = mock.Mock()
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary_1 = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary_1
        network_1._moId = 1

        network_2 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_2_name_property = mock.PropertyMock(return_value='test_network_2')
        type(network_2).name = network_2_name_property
        expected_sumary_2 = {
            'network': {
                '_moId': 2
            }
        }
        network_2.summary = expected_sumary_2
        network_2._moId = 2

        mock_view = mock.Mock(view=[network_1, network_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_network',
                'id': 1,
                'is_dvs': False,
                'summary': expected_sumary_1
            }, {
                'name': 'test_network_2',
                'id': 2,
                'is_dvs': True,
                'summary': expected_sumary_2
            }
        ]

        result = self._action.get_all()
        self.assertEqual(result, expected_result)

    def test_run_get_by_id_or_name(self):
        network_1 = mock.Mock()
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary_1 = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary_1
        network_1._moId = 1

        network_2 = mock.Mock()
        network_2_name_property = mock.PropertyMock(return_value='test_network_2')
        type(network_2).name = network_2_name_property
        expected_sumary_2 = {
            'network': {
                '_moId': 2
            }
        }
        network_2.summary = expected_sumary_2
        network_2._moId = 2

        network_3 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_3_name_property = mock.PropertyMock(return_value='test_network_3')
        type(network_3).name = network_3_name_property
        expected_sumary_3 = {
            'network': {
                '_moId': 3
            }
        }
        network_3.summary = expected_sumary_3
        network_3._moId = 3

        network_4 = mock.Mock()
        network_4_name_property = mock.PropertyMock(return_value='test_network_4')
        type(network_4).name = network_4_name_property
        expected_sumary_4 = {
            'network': {
                '_moId': 4
            }
        }
        network_4.summary = expected_sumary_4
        network_4._moId = 4

        network_5 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_5_name_property = mock.PropertyMock(return_value='test_network_5')
        type(network_5).name = network_5_name_property
        expected_sumary_5 = {
            'network': {
                '_moId': 5
            }
        }
        network_5.summary = expected_sumary_5
        network_5._moId = 5

        mock_view = mock.Mock(view=[network_1,
                                    network_2,
                                    network_3,
                                    network_4,
                                    network_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_network_4',
                'id': 4,
                'is_dvs': False,
                'summary': expected_sumary_4
            }, {
                'name': 'test_network_2',
                'id': 2,
                'is_dvs': False,
                'summary': expected_sumary_2
            }, {
                'name': 'test_network_5',
                'id': 5,
                'is_dvs': True,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run([4], ['test_network_2', 'test_network_5'])
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        network_1 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_1_name_property = mock.PropertyMock(return_value='test_network')
        type(network_1).name = network_1_name_property
        expected_sumary_1 = {
            'network': {
                '_moId': 1
            }
        }
        network_1.summary = expected_sumary_1
        network_1._moId = 1

        network_2 = mock.Mock()
        network_2_name_property = mock.PropertyMock(return_value='test_network_2')
        type(network_2).name = network_2_name_property
        expected_sumary_2 = {
            'network': {
                '_moId': 2
            }
        }
        network_2.summary = expected_sumary_2
        network_2._moId = 2

        network_3 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_3_name_property = mock.PropertyMock(return_value='test_network_3')
        type(network_3).name = network_3_name_property
        expected_sumary_3 = {
            'network': {
                '_moId': 3
            }
        }
        network_3.summary = expected_sumary_3
        network_3._moId = 3

        network_4 = mock.Mock()
        network_4_name_property = mock.PropertyMock(return_value='test_network_4')
        type(network_4).name = network_4_name_property
        expected_sumary_4 = {
            'network': {
                '_moId': 4
            }
        }
        network_4.summary = expected_sumary_4
        network_4._moId = 4

        network_5 = mock.Mock(spec=vim.dvs.DistributedVirtualPortgroup)
        network_5_name_property = mock.PropertyMock(return_value='test_network_5')
        type(network_5).name = network_5_name_property
        expected_sumary_5 = {
            'network': {
                '_moId': 5
            }
        }
        network_5.summary = expected_sumary_5
        network_5._moId = 5

        mock_view = mock.Mock(view=[network_1,
                                    network_2,
                                    network_3,
                                    network_4,
                                    network_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_network',
                'id': 1,
                'is_dvs': True,
                'summary': expected_sumary_1
            }, {
                'name': 'test_network_2',
                'id': 2,
                'is_dvs': False,
                'summary': expected_sumary_2
            }, {
                'name': 'test_network_3',
                'id': 3,
                'is_dvs': True,
                'summary': expected_sumary_3
            }, {
                'name': 'test_network_4',
                'id': 4,
                'is_dvs': False,
                'summary': expected_sumary_4
            }, {
                'name': 'test_network_5',
                'id': 5,
                'is_dvs': True,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run(None, None)
        self.assertEqual(result, expected_result)
