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
from cluster_get import ClusterGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'ClusterGet'
]


class ClusterGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = ClusterGet

    def setUp(self):
        super(ClusterGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_cluster_dict(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary = {'numHosts': '1'}
        cluster_1.summary = expected_summary
        cluster_1._moId = 1

        expected_result = {
            'name': 'test_cluster',
            'id': '1',
            'summary': expected_summary
        }

        result = self._action.get_cluster_dict(cluster_1)
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary_1 = {'numHosts': '1'}
        cluster_1.summary = expected_summary_1
        cluster_1._moId = 1

        cluster_2 = mock.Mock()
        cluster_2.__str__ = mock.Mock(return_value="''vim.Cluster:2''")
        cluster_2_name_property = mock.PropertyMock(return_value='test_cluster_2')
        type(cluster_2).name = cluster_2_name_property
        expected_summary_2 = {'numHosts': '1'}
        cluster_2.summary = expected_summary_2
        cluster_2._moId = 2

        cluster_3 = mock.Mock()
        cluster_3.__str__ = mock.Mock(return_value="''vim.Cluster:3''")
        cluster_3_name_property = mock.PropertyMock(return_value='test_cluster_3')
        type(cluster_3).name = cluster_3_name_property
        expected_summary_3 = {'numHosts': '1'}
        cluster_3.summary = expected_summary_3
        cluster_3._moId = 3

        cluster_4 = mock.Mock()
        cluster_4.__str__ = mock.Mock(return_value="''vim.Cluster:4''")
        cluster_4_name_property = mock.PropertyMock(return_value='test_cluster_4')
        type(cluster_4).name = cluster_4_name_property
        expected_summary_4 = {'numHosts': '1'}
        cluster_4.summary = expected_summary_4
        cluster_4._moId = 4

        cluster_5 = mock.Mock()
        cluster_5.__str__ = mock.Mock(return_value="''vim.Cluster:5''")
        cluster_5_name_property = mock.PropertyMock(return_value='test_cluster_5')
        type(cluster_5).name = cluster_5_name_property
        expected_summary_5 = {'numHosts': '1'}
        cluster_5.summary = expected_summary_5
        cluster_5._moId = 5

        mock_view = mock.Mock(view=[cluster_1,
                                    cluster_2,
                                    cluster_3,
                                    cluster_4,
                                    cluster_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_cluster_4',
                'id': '4',
                'summary': expected_summary_4
            }, {
                'name': 'test_cluster_2',
                'id': '2',
                'summary': expected_summary_2
            }, {
                'name': 'test_cluster_5',
                'id': '5',
                'summary': expected_summary_5
            }
        ]

        result = self._action.get_by_id_or_name([4], ['test_cluster_2', 'test_cluster_5'])
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name_duplicate(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary_1 = {'numHosts': '1'}
        cluster_1.summary = expected_summary_1
        cluster_1._moId = 1

        mock_view = mock.Mock(view=[cluster_1])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_cluster',
                'id': '1',
                'summary': expected_summary_1
            }
        ]

        result = self._action.get_by_id_or_name([1], ['test_cluster'])
        self.assertEqual(result, expected_result)

    def test_get_all_clusters(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary_1 = {'numHosts': '1'}
        cluster_1.summary = expected_summary_1
        cluster_1._moId = 1

        cluster_2 = mock.Mock()
        cluster_2.__str__ = mock.Mock(return_value="''vim.Cluster:2''")
        cluster_2_name_property = mock.PropertyMock(return_value='test_cluster_2')
        type(cluster_2).name = cluster_2_name_property
        expected_summary_2 = {'numHosts': '1'}
        cluster_2.summary = expected_summary_2
        cluster_2._moId = 2

        mock_view = mock.Mock(view=[cluster_1, cluster_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_cluster',
                'id': '1',
                'summary': expected_summary_1
            }, {
                'name': 'test_cluster_2',
                'id': '2',
                'summary': expected_summary_2
            }
        ]

        result = self._action.get_all()
        self.assertEqual(result, expected_result)

    def test_run_get_by_id_or_name(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary_1 = {'numHosts': '1'}
        cluster_1.summary = expected_summary_1
        cluster_1._moId = 1

        cluster_2 = mock.Mock()
        cluster_2.__str__ = mock.Mock(return_value="''vim.Cluster:2''")
        cluster_2_name_property = mock.PropertyMock(return_value='test_cluster_2')
        type(cluster_2).name = cluster_2_name_property
        expected_summary_2 = {'numHosts': '1'}
        cluster_2.summary = expected_summary_2
        cluster_2._moId = 2

        cluster_3 = mock.Mock()
        cluster_3.__str__ = mock.Mock(return_value="''vim.Cluster:3''")
        cluster_3_name_property = mock.PropertyMock(return_value='test_cluster_3')
        type(cluster_3).name = cluster_3_name_property
        expected_summary_3 = {'numHosts': '1'}
        cluster_3.summary = expected_summary_3
        cluster_3._moId = 3

        cluster_4 = mock.Mock()
        cluster_4.__str__ = mock.Mock(return_value="''vim.Cluster:4''")
        cluster_4_name_property = mock.PropertyMock(return_value='test_cluster_4')
        type(cluster_4).name = cluster_4_name_property
        expected_summary_4 = {'numHosts': '1'}
        cluster_4.summary = expected_summary_4
        cluster_4._moId = 4

        cluster_5 = mock.Mock()
        cluster_5.__str__ = mock.Mock(return_value="''vim.Cluster:5''")
        cluster_5_name_property = mock.PropertyMock(return_value='test_cluster_5')
        type(cluster_5).name = cluster_5_name_property
        expected_summary_5 = {'numHosts': '1'}
        cluster_5.summary = expected_summary_5
        cluster_5._moId = 5

        mock_view = mock.Mock(view=[cluster_1,
                                    cluster_2,
                                    cluster_3,
                                    cluster_4,
                                    cluster_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_cluster_4',
                'id': '4',
                'summary': expected_summary_4
            }, {
                'name': 'test_cluster_2',
                'id': '2',
                'summary': expected_summary_2
            }, {
                'name': 'test_cluster_5',
                'id': '5',
                'summary': expected_summary_5
            }
        ]

        result = self._action.run([4], ['test_cluster_2', 'test_cluster_5'])
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        cluster_1 = mock.Mock()
        cluster_1.__str__ = mock.Mock(return_value="''vim.Cluster:1''")
        cluster_1_name_property = mock.PropertyMock(return_value='test_cluster')
        type(cluster_1).name = cluster_1_name_property
        expected_summary_1 = {'numHosts': '1'}
        cluster_1.summary = expected_summary_1
        cluster_1._moId = 1

        cluster_2 = mock.Mock()
        cluster_2.__str__ = mock.Mock(return_value="''vim.Cluster:2''")
        cluster_2_name_property = mock.PropertyMock(return_value='test_cluster_2')
        type(cluster_2).name = cluster_2_name_property
        expected_summary_2 = {'numHosts': '1'}
        cluster_2.summary = expected_summary_2
        cluster_2._moId = 2

        cluster_3 = mock.Mock()
        cluster_3.__str__ = mock.Mock(return_value="''vim.Cluster:3''")
        cluster_3_name_property = mock.PropertyMock(return_value='test_cluster_3')
        type(cluster_3).name = cluster_3_name_property
        expected_summary_3 = {'numHosts': '1'}
        cluster_3.summary = expected_summary_3
        cluster_3._moId = 3

        cluster_4 = mock.Mock()
        cluster_4.__str__ = mock.Mock(return_value="''vim.Cluster:4''")
        cluster_4_name_property = mock.PropertyMock(return_value='test_cluster_4')
        type(cluster_4).name = cluster_4_name_property
        expected_summary_4 = {'numHosts': '1'}
        cluster_4.summary = expected_summary_4
        cluster_4._moId = 4

        cluster_5 = mock.Mock()
        cluster_5.__str__ = mock.Mock(return_value="''vim.Cluster:5''")
        cluster_5_name_property = mock.PropertyMock(return_value='test_cluster_5')
        type(cluster_5).name = cluster_5_name_property
        expected_summary_5 = {'numHosts': '1'}
        cluster_5.summary = expected_summary_5
        cluster_5._moId = 5

        mock_view = mock.Mock(view=[cluster_1,
                                    cluster_2,
                                    cluster_3,
                                    cluster_4,
                                    cluster_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_cluster',
                'id': '1',
                'summary': expected_summary_1
            }, {
                'name': 'test_cluster_2',
                'id': '2',
                'summary': expected_summary_2
            }, {
                'name': 'test_cluster_3',
                'id': '3',
                'summary': expected_summary_3
            }, {
                'name': 'test_cluster_4',
                'id': '4',
                'summary': expected_summary_4
            }, {
                'name': 'test_cluster_5',
                'id': '5',
                'summary': expected_summary_5
            }
        ]

        result = self._action.run(None, None)
        self.assertEqual(result, expected_result)
