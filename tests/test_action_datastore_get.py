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
from datastore_get import DatastoreGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'DatastoreGet'
]


class DatastoreGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = DatastoreGet

    def setUp(self):
        super(DatastoreGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_datastore_dict(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary
        datastore_1._moId = 1

        expected_result = {
            'name': 'test_datastore',
            'id': 1,
            'summary': expected_sumary
        }

        result = self._action.get_datastore_dict(datastore_1)
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary_1 = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary_1
        datastore_1._moId = 1

        datastore_2 = mock.Mock()
        datastore_2_name_property = mock.PropertyMock(return_value='test_datastore_2')
        type(datastore_2).name = datastore_2_name_property
        expected_sumary_2 = {
            'datastore': {
                '_moId': 2
            }
        }
        datastore_2.summary = expected_sumary_2
        datastore_2._moId = 2

        datastore_3 = mock.Mock()
        datastore_3_name_property = mock.PropertyMock(return_value='test_datastore_3')
        type(datastore_3).name = datastore_3_name_property
        expected_sumary_3 = {
            'datastore': {
                '_moId': 3
            }
        }
        datastore_3.summary = expected_sumary_3
        datastore_3._moId = 3

        datastore_4 = mock.Mock()
        datastore_4_name_property = mock.PropertyMock(return_value='test_datastore_4')
        type(datastore_4).name = datastore_4_name_property
        expected_sumary_4 = {
            'datastore': {
                '_moId': 4
            }
        }
        datastore_4.summary = expected_sumary_4
        datastore_4._moId = 4

        datastore_5 = mock.Mock()
        datastore_5_name_property = mock.PropertyMock(return_value='test_datastore_5')
        type(datastore_5).name = datastore_5_name_property
        expected_sumary_5 = {
            'datastore': {
                '_moId': 5
            }
        }
        datastore_5.summary = expected_sumary_5
        datastore_5._moId = 5

        mock_view = mock.Mock(view=[datastore_1,
                                    datastore_2,
                                    datastore_3,
                                    datastore_4,
                                    datastore_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datastore_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_datastore_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_datastore_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.get_by_id_or_name([4], ['test_datastore_2', 'test_datastore_5'])
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name_duplicate(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary_1 = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary_1
        datastore_1._moId = 1

        mock_view = mock.Mock(view=[datastore_1])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datastore',
                'id': 1,
                'summary': expected_sumary_1
            }
        ]

        result = self._action.get_by_id_or_name([1], ['test_datastore'])
        self.assertEqual(result, expected_result)

    def test_get_all_datastores(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary_1 = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary_1
        datastore_1._moId = 1

        datastore_2 = mock.Mock()
        datastore_2_name_property = mock.PropertyMock(return_value='test_datastore_2')
        type(datastore_2).name = datastore_2_name_property
        expected_sumary_2 = {
            'datastore': {
                '_moId': 2
            }
        }
        datastore_2.summary = expected_sumary_2
        datastore_2._moId = 2

        mock_view = mock.Mock(view=[datastore_1, datastore_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datastore',
                'id': 1,
                'summary': expected_sumary_1
            }, {
                'name': 'test_datastore_2',
                'id': 2,
                'summary': expected_sumary_2
            }
        ]

        result = self._action.get_all()
        self.assertEqual(result, expected_result)

    def test_run_get_by_id_or_name(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary_1 = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary_1
        datastore_1._moId = 1

        datastore_2 = mock.Mock()
        datastore_2_name_property = mock.PropertyMock(return_value='test_datastore_2')
        type(datastore_2).name = datastore_2_name_property
        expected_sumary_2 = {
            'datastore': {
                '_moId': 2
            }
        }
        datastore_2.summary = expected_sumary_2
        datastore_2._moId = 2

        datastore_3 = mock.Mock()
        datastore_3_name_property = mock.PropertyMock(return_value='test_datastore_3')
        type(datastore_3).name = datastore_3_name_property
        expected_sumary_3 = {
            'datastore': {
                '_moId': 3
            }
        }
        datastore_3.summary = expected_sumary_3
        datastore_3._moId = 3

        datastore_4 = mock.Mock()
        datastore_4_name_property = mock.PropertyMock(return_value='test_datastore_4')
        type(datastore_4).name = datastore_4_name_property
        expected_sumary_4 = {
            'datastore': {
                '_moId': 4
            }
        }
        datastore_4.summary = expected_sumary_4
        datastore_4._moId = 4

        datastore_5 = mock.Mock()
        datastore_5_name_property = mock.PropertyMock(return_value='test_datastore_5')
        type(datastore_5).name = datastore_5_name_property
        expected_sumary_5 = {
            'datastore': {
                '_moId': 5
            }
        }
        datastore_5.summary = expected_sumary_5
        datastore_5._moId = 5

        mock_view = mock.Mock(view=[datastore_1,
                                    datastore_2,
                                    datastore_3,
                                    datastore_4,
                                    datastore_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datastore_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_datastore_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_datastore_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run([4], ['test_datastore_2', 'test_datastore_5'])
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        datastore_1 = mock.Mock()
        datastore_1_name_property = mock.PropertyMock(return_value='test_datastore')
        type(datastore_1).name = datastore_1_name_property
        expected_sumary_1 = {
            'datastore': {
                '_moId': 1
            }
        }
        datastore_1.summary = expected_sumary_1
        datastore_1._moId = 1

        datastore_2 = mock.Mock()
        datastore_2_name_property = mock.PropertyMock(return_value='test_datastore_2')
        type(datastore_2).name = datastore_2_name_property
        expected_sumary_2 = {
            'datastore': {
                '_moId': 2
            }
        }
        datastore_2.summary = expected_sumary_2
        datastore_2._moId = 2

        datastore_3 = mock.Mock()
        datastore_3_name_property = mock.PropertyMock(return_value='test_datastore_3')
        type(datastore_3).name = datastore_3_name_property
        expected_sumary_3 = {
            'datastore': {
                '_moId': 3
            }
        }
        datastore_3.summary = expected_sumary_3
        datastore_3._moId = 3

        datastore_4 = mock.Mock()
        datastore_4_name_property = mock.PropertyMock(return_value='test_datastore_4')
        type(datastore_4).name = datastore_4_name_property
        expected_sumary_4 = {
            'datastore': {
                '_moId': 4
            }
        }
        datastore_4.summary = expected_sumary_4
        datastore_4._moId = 4

        datastore_5 = mock.Mock()
        datastore_5_name_property = mock.PropertyMock(return_value='test_datastore_5')
        type(datastore_5).name = datastore_5_name_property
        expected_sumary_5 = {
            'datastore': {
                '_moId': 5
            }
        }
        datastore_5.summary = expected_sumary_5
        datastore_5._moId = 5

        mock_view = mock.Mock(view=[datastore_1,
                                    datastore_2,
                                    datastore_3,
                                    datastore_4,
                                    datastore_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_datastore',
                'id': 1,
                'summary': expected_sumary_1
            }, {
                'name': 'test_datastore_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_datastore_3',
                'id': 3,
                'summary': expected_sumary_3
            }, {
                'name': 'test_datastore_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_datastore_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run(None, None)
        self.assertEqual(result, expected_result)
