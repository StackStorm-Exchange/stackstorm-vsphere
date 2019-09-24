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
from vm_bestfit import BestFit
from st2common.runners.base_action import Action
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'BestFitTestCase'
]


class BestFitTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = BestFit

    def setUp(self):
        super(BestFitTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_init(self):
        action = self.get_action_instance(self.new_config)
        self.assertIsInstance(action, BestFit)
        self.assertIsInstance(action, Action)

    def test_filter_datastores_regex_match(self):
        test_filters = ["(?i)(iso)"]
        test_name = "dev_isos"
        expected_result = False
        result = self._action.filter_datastores(test_name, test_filters)
        self.assertEqual(expected_result, result)

    def test_filter_datastores_regex_no_match(self):
        test_filters = ["(?i)(iso)"]
        test_name = "testdatastore"
        expected_result = True
        result = self._action.filter_datastores(test_name, test_filters)
        self.assertEqual(expected_result, result)

    def test_filter_datastores_name_match(self):
        test_filters = ["dev_isos"]
        test_name = "dev_isos"
        expected_result = False
        result = self._action.filter_datastores(test_name, test_filters)
        self.assertEqual(expected_result, result)

    def test_filter_datastores_name_no_match(self):
        test_filters = ["dev_isos"]
        test_name = "testdatastore"
        expected_result = True
        result = self._action.filter_datastores(test_name, test_filters)
        self.assertEqual(expected_result, result)

    @mock.patch('vmwarelib.inventory.get_managed_entities')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_host_none_available(self, mock_vim_type, mock_entities):
        test_cluster_name = "cls1"
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        # Mock function results
        mock_host1 = mock.MagicMock()
        mock_host1.parent.name = "cls2"

        mock_host2 = mock.MagicMock()
        mock_host2.parent.name = "cls1"
        mock_host2.runtime.powerState = "poweredOff"

        # Mock a list of 2 hosts that are unavailable
        test_host_list = [mock_host1, mock_host2]
        mock_host_list = mock.MagicMock(view=test_host_list)
        mock_entities.return_value = mock_host_list

        with self.assertRaises(Exception):
            self._action.get_host(test_cluster_name)

            mock_entities.assert_called_with(self._action.si_content, test_vim_type)

    @mock.patch('vmwarelib.inventory.get_managed_entities')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_host(self, mock_vim_type, mock_entities):
        test_cluster_name = "cls1"
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        # Mock function results
        mock_host1 = mock.MagicMock()
        mock_host1.parent.name = "cls1"
        mock_host1.runtime.powerState = "poweredOn"
        mock_host1.runtime.inMaintenanceMode = False
        mock_host1.vm = ["vm1", "vm2"]

        mock_host2 = mock.MagicMock()
        mock_host2.parent.name = "cls1"
        mock_host2.runtime.powerState = "poweredOn"
        mock_host2.runtime.inMaintenanceMode = False
        # This host will be the expected result since it has the fewest VMs
        mock_host2.vm = ["vm1"]

        # Mock a list of 2 hosts that are unavailable
        test_host_list = [mock_host1, mock_host2]
        mock_host_list = mock.MagicMock(view=test_host_list)
        mock_entities.return_value = mock_host_list

        result = self._action.get_host(test_cluster_name)

        self.assertEqual(result, mock_host2)
        mock_entities.assert_called_with(self._action.si_content, test_vim_type)

    @mock.patch('vmwarelib.inventory.get_managed_entity')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_storage_not_found(self, mock_vim_type, mock_entity):
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        test_host = mock.MagicMock()
        test_datastore_filter = ["filter"]
        test_disks = [{"datastore": "fail"}]

        # invoke action with invalid names which don't match any objects
        mock_entity.side_effect = Exception("Inventory Error: Unable to Find Object in a test")
        with self.assertRaises(Exception):
            self._action.get_storage(test_host, test_datastore_filter, test_disks)

    @mock.patch('vmwarelib.inventory.get_managed_entity')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_storage_from_disk(self, mock_vim_type, mock_entity):
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        test_datastore_filter = ["filter"]
        test_disks = [{"datastore": "test-ds-1"}]

        expected_result = "result"

        mock_host = mock.MagicMock()

        mock_entity.return_value = expected_result

        result = self._action.get_storage(mock_host, test_datastore_filter, test_disks)

        self.assertEqual(expected_result, result)
        mock_entity.assert_called_with(self._action.si_content, test_vim_type, name="test-ds-1")

    @mock.patch('vm_bestfit.BestFit.filter_datastores')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_storage_no_disk(self, mock_vim_type, mock_filter):
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        test_datastore_filter = ["(?i)(filter)"]
        test_disks = None

        # Mock datastore objects
        mock_ds1 = mock.MagicMock()
        type(mock_ds1).name = mock.PropertyMock(return_value="test-ds-1")
        mock_ds1.summary.maintenanceMode = 'normal'
        mock_ds1.info.freeSpace = 10

        mock_ds2 = mock.MagicMock()
        type(mock_ds2).name = mock.PropertyMock(return_value="test-ds-2")
        mock_ds2.summary.maintenanceMode = 'normal'
        mock_ds2.info.freeSpace = 20

        # This datastre should get filtered out from test_datastore_filter
        mock_ds3 = mock.MagicMock()
        type(mock_ds3).name = mock.PropertyMock(return_value="test-ds-filter")
        mock_ds3.summary.maintenanceMode = 'normal'
        mock_ds3.info.freeSpace = 100

        # This is the result from filter_datastores function that filters out mock_ds3
        mock_filter.side_effect = [True, True, False]

        # Mock a list of 2 hosts that are unavailable
        test_ds_list = [mock_ds1, mock_ds2, mock_ds3]

        # Mock host input
        mock_host = mock.MagicMock(datastore=test_ds_list)

        result = self._action.get_storage(mock_host, test_datastore_filter, test_disks)

        self.assertEqual(result, mock_ds2)
        mock_filter.assert_has_calls([mock.call("test-ds-1", test_datastore_filter),
                                      mock.call("test-ds-2", test_datastore_filter),
                                      mock.call("test-ds-filter", test_datastore_filter)])

    @mock.patch('vm_bestfit.BestFit.filter_datastores')
    @mock.patch('vmwarelib.actions.BaseAction.get_vim_type')
    def test_get_storage_skip_maintenance_mode(self, mock_vim_type, mock_filter):
        test_vim_type = "vimType"
        mock_vim_type.return_value = test_vim_type

        test_datastore_filter = []
        test_disks = None

        # Mock datastore objects
        mock_ds1 = mock.MagicMock()
        mock_ds1.name = "test-ds-1"
        mock_ds1.summary.maintenanceMode = 'enteringMaintenance'
        mock_ds1.info.freeSpace = 10

        mock_ds2 = mock.MagicMock()
        mock_ds2.name = "test-ds-2"
        mock_ds2.summary.maintenanceMode = 'inMaintenance'
        mock_ds2.info.freeSpace = 20

        # This datastre should get filtered out from test_datastore_filter
        mock_ds3 = mock.MagicMock()
        mock_ds3.name = "test-ds-3"
        mock_ds3.summary.maintenanceMode = 'normal'
        mock_ds3.info.freeSpace = 100

        # Don't filter anything by name
        mock_filter.side_effect = [True, True, True]

        # Mock a list of 2 hosts that are unavailable
        test_ds_list = [mock_ds1, mock_ds2, mock_ds3]

        # Mock host input
        mock_host = mock.MagicMock(datastore=test_ds_list)

        result = self._action.get_storage(mock_host, test_datastore_filter, test_disks)

        # mock_ds3 is the only one where maintenanceMode == 'normal'
        self.assertEqual(result, mock_ds3)

        # we should have only called filter on one datastore, the maintenance mode
        # check should have kicked out before testing the other datastores
        mock_filter.assert_has_calls([mock.call("test-ds-3", test_datastore_filter)])

    @mock.patch('vm_bestfit.BestFit.get_storage')
    @mock.patch('vm_bestfit.BestFit.get_host')
    def test_run(self, mock_get_host, mock_get_storage):
        # Define test variables
        test_ds_filter = ["filter"]
        test_disks = [{"datastore": "test-ds-1"}]
        test_vsphere = "vsphere"

        test_cluster_name = "test-cluster"
        test_host_name = "test-host"
        test_host_id = "host-123"
        test_ds_name = "test-ds"
        test_ds_id = "ds-123"

        self._action.establish_connection = mock.Mock()

        # Mock host and datastore result objects
        mock_host = mock.MagicMock()
        type(mock_host).name = mock.PropertyMock(return_value=test_host_name)
        mock_host.parent.name = test_cluster_name
        mock_host._moId = test_host_id

        mock_get_host.return_value = mock_host

        mock_ds = mock.MagicMock()
        type(mock_ds).name = mock.PropertyMock(return_value=test_ds_name)
        mock_ds._moId = test_ds_id

        mock_get_storage.return_value = mock_ds

        expected_result = {'clusterName': test_cluster_name,
                           'hostName': test_host_name,
                           'hostID': test_host_id,
                           'datastoreName': test_ds_name,
                           'datastoreID': test_ds_id}

        result = self._action.run(test_cluster_name, test_ds_filter, test_disks, test_vsphere)

        self.assertEqual(result, expected_result)
        self._action.establish_connection.assert_called_with(test_vsphere)
        mock_get_host.assert_called_with(test_cluster_name)
        mock_get_storage.assert_called_with(mock_host, test_ds_filter, test_disks)
