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
from datacenter_get import DatacenterGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'DatacenterGet'
]


class DatacenterGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = DatacenterGet

    def setUp(self):
        super(DatacenterGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_datacenter_dict(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration
        datacenter_1._moId = 1

        expected_result = {
            'name': 'test_datacenter',
            'id': '1',
            'configuration': expected_configuration
        }

        result = self._action.get_datacenter_dict(datacenter_1)
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration_1 = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration_1
        datacenter_1._moId = 1

        datacenter_2 = mock.Mock()
        datacenter_2.__str__ = mock.Mock(return_value="''vim.Datacenter:2''")
        datacenter_2_name_property = mock.PropertyMock(return_value='test_datacenter_2')
        type(datacenter_2).name = datacenter_2_name_property
        expected_configuration_2 = {'defaultHardwareVersionKey': 'test'}
        datacenter_2.configuration = expected_configuration_2
        datacenter_2._moId = 2

        datacenter_3 = mock.Mock()
        datacenter_3.__str__ = mock.Mock(return_value="''vim.Datacenter:3''")
        datacenter_3_name_property = mock.PropertyMock(return_value='test_datacenter_3')
        type(datacenter_3).name = datacenter_3_name_property
        expected_configuration_3 = {'defaultHardwareVersionKey': 'test'}
        datacenter_3.configuration = expected_configuration_3
        datacenter_3._moId = 3

        datacenter_4 = mock.Mock()
        datacenter_4.__str__ = mock.Mock(return_value="''vim.Datacenter:4''")
        datacenter_4_name_property = mock.PropertyMock(return_value='test_datacenter_4')
        type(datacenter_4).name = datacenter_4_name_property
        expected_configuration_4 = {'defaultHardwareVersionKey': 'test'}
        datacenter_4.configuration = expected_configuration_4
        datacenter_4._moId = 4

        datacenter_5 = mock.Mock()
        datacenter_5.__str__ = mock.Mock(return_value="''vim.Datacenter:5''")
        datacenter_5_name_property = mock.PropertyMock(return_value='test_datacenter_5')
        type(datacenter_5).name = datacenter_5_name_property
        expected_configuration_5 = {'defaultHardwareVersionKey': 'test'}
        datacenter_5.configuration = expected_configuration_5
        datacenter_5._moId = 5

        mock_view = mock.Mock(view=[datacenter_1,
                                    datacenter_2,
                                    datacenter_3,
                                    datacenter_4,
                                    datacenter_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datacenter_4',
                'id': '4',
                'configuration': expected_configuration_4
            }, {
                'name': 'test_datacenter_5',
                'id': '5',
                'configuration': expected_configuration_5
            }, {
                'name': 'test_datacenter_2',
                'id': '2',
                'configuration': expected_configuration_2
            }
        ]

        result = self._action.get_by_id_or_name([4], ['test_datacenter_2', 'test_datacenter_5'])
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name_duplicate(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration_1 = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration_1
        datacenter_1._moId = 1

        mock_view = mock.Mock(view=[datacenter_1])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datacenter',
                'id': '1',
                'configuration': expected_configuration_1
            }
        ]

        result = self._action.get_by_id_or_name([1], ['test_datacenter'])
        self.assertEqual(result, expected_result)

    def test_get_all_datacenters(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration_1 = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration_1
        datacenter_1._moId = 1

        datacenter_2 = mock.Mock()
        datacenter_2.__str__ = mock.Mock(return_value="''vim.Datacenter:2''")
        datacenter_2_name_property = mock.PropertyMock(return_value='test_datacenter_2')
        type(datacenter_2).name = datacenter_2_name_property
        expected_configuration_2 = {'defaultHardwareVersionKey': 'test'}
        datacenter_2.configuration = expected_configuration_2
        datacenter_2._moId = 2

        mock_view = mock.Mock(view=[datacenter_1, datacenter_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datacenter',
                'id': '1',
                'configuration': expected_configuration_1
            }, {
                'name': 'test_datacenter_2',
                'id': '2',
                'configuration': expected_configuration_2
            }
        ]

        result = self._action.get_all()
        self.assertEqual(result, expected_result)

    def test_run_get_by_id_or_name(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration_1 = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration_1
        datacenter_1._moId = 1

        datacenter_2 = mock.Mock()
        datacenter_2.__str__ = mock.Mock(return_value="''vim.Datacenter:2''")
        datacenter_2_name_property = mock.PropertyMock(return_value='test_datacenter_2')
        type(datacenter_2).name = datacenter_2_name_property
        expected_configuration_2 = {'defaultHardwareVersionKey': 'test'}
        datacenter_2.configuration = expected_configuration_2
        datacenter_2._moId = 2

        datacenter_3 = mock.Mock()
        datacenter_3.__str__ = mock.Mock(return_value="''vim.Datacenter:3''")
        datacenter_3_name_property = mock.PropertyMock(return_value='test_datacenter_3')
        type(datacenter_3).name = datacenter_3_name_property
        expected_configuration_3 = {'defaultHardwareVersionKey': 'test'}
        datacenter_3.configuration = expected_configuration_3
        datacenter_3._moId = 3

        datacenter_4 = mock.Mock()
        datacenter_4.__str__ = mock.Mock(return_value="''vim.Datacenter:4''")
        datacenter_4_name_property = mock.PropertyMock(return_value='test_datacenter_4')
        type(datacenter_4).name = datacenter_4_name_property
        expected_configuration_4 = {'defaultHardwareVersionKey': 'test'}
        datacenter_4.configuration = expected_configuration_4
        datacenter_4._moId = 4

        datacenter_5 = mock.Mock()
        datacenter_5.__str__ = mock.Mock(return_value="''vim.Datacenter:5''")
        datacenter_5_name_property = mock.PropertyMock(return_value='test_datacenter_5')
        type(datacenter_5).name = datacenter_5_name_property
        expected_configuration_5 = {'defaultHardwareVersionKey': 'test'}
        datacenter_5.configuration = expected_configuration_5
        datacenter_5._moId = 5

        mock_view = mock.Mock(view=[datacenter_1,
                                    datacenter_2,
                                    datacenter_3,
                                    datacenter_4,
                                    datacenter_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datacenter_4',
                'id': '4',
                'configuration': expected_configuration_4
            }, {
                'name': 'test_datacenter_5',
                'id': '5',
                'configuration': expected_configuration_5
            }, {
                'name': 'test_datacenter_2',
                'id': '2',
                'configuration': expected_configuration_2
            }
        ]

        result = self._action.run([4], ['test_datacenter_2', 'test_datacenter_5'])
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        datacenter_1 = mock.Mock()
        datacenter_1.__str__ = mock.Mock(return_value="''vim.Datacenter:1''")
        datacenter_1_name_property = mock.PropertyMock(return_value='test_datacenter')
        type(datacenter_1).name = datacenter_1_name_property
        expected_configuration_1 = {'defaultHardwareVersionKey': 'test'}
        datacenter_1.configuration = expected_configuration_1
        datacenter_1._moId = 1

        datacenter_2 = mock.Mock()
        datacenter_2.__str__ = mock.Mock(return_value="''vim.Datacenter:2''")
        datacenter_2_name_property = mock.PropertyMock(return_value='test_datacenter_2')
        type(datacenter_2).name = datacenter_2_name_property
        expected_configuration_2 = {'defaultHardwareVersionKey': 'test'}
        datacenter_2.configuration = expected_configuration_2
        datacenter_2._moId = 2

        datacenter_3 = mock.Mock()
        datacenter_3.__str__ = mock.Mock(return_value="''vim.Datacenter:3''")
        datacenter_3_name_property = mock.PropertyMock(return_value='test_datacenter_3')
        type(datacenter_3).name = datacenter_3_name_property
        expected_configuration_3 = {'defaultHardwareVersionKey': 'test'}
        datacenter_3.configuration = expected_configuration_3
        datacenter_3._moId = 3

        datacenter_4 = mock.Mock()
        datacenter_4.__str__ = mock.Mock(return_value="''vim.Datacenter:4''")
        datacenter_4_name_property = mock.PropertyMock(return_value='test_datacenter_4')
        type(datacenter_4).name = datacenter_4_name_property
        expected_configuration_4 = {'defaultHardwareVersionKey': 'test'}
        datacenter_4.configuration = expected_configuration_4
        datacenter_4._moId = 4

        datacenter_5 = mock.Mock()
        datacenter_5.__str__ = mock.Mock(return_value="''vim.Datacenter:5''")
        datacenter_5_name_property = mock.PropertyMock(return_value='test_datacenter_5')
        type(datacenter_5).name = datacenter_5_name_property
        expected_configuration_5 = {'defaultHardwareVersionKey': 'test'}
        datacenter_5.configuration = expected_configuration_5
        datacenter_5._moId = 5

        mock_view = mock.Mock(view=[datacenter_1,
                                    datacenter_2,
                                    datacenter_3,
                                    datacenter_4,
                                    datacenter_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datacenter',
                'id': '1',
                'configuration': expected_configuration_1
            }, {
                'name': 'test_datacenter_2',
                'id': '2',
                'configuration': expected_configuration_2
            }, {
                'name': 'test_datacenter_3',
                'id': '3',
                'configuration': expected_configuration_3
            }, {
                'name': 'test_datacenter_4',
                'id': '4',
                'configuration': expected_configuration_4
            }, {
                'name': 'test_datacenter_5',
                'id': '5',
                'configuration': expected_configuration_5
            }
        ]

        result = self._action.run(None, None)
        self.assertEqual(result, expected_result)
