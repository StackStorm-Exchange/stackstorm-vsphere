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
from vm_snapshots_delete import VMSnapshotsDelete
from vsphere_base_action_test_case import VsphereBaseActionTestCase
import re

__all__ = [
    'VMSnapshotsDeleteTestCase'
]


class VMSnapshotsDeleteTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMSnapshotsDelete

    def setUp(self):
        super(VMSnapshotsDeleteTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch('vm_snapshots_delete.re.compile')
    def test_compile_regexes(self, mock_compile):
        # def test_compile_regexes(self):
        test_regex_list = ["REGEX1", "REGEX2"]
        expected_result = ["PATTERN1", "PATTERN2"]
        mock_compile.side_effect = expected_result
        result = self._action.compile_regexes(test_regex_list)

        self.assertEqual(result, expected_result)

        calls = [mock.call("REGEX1"), mock.call("REGEX2")]
        mock_compile.assert_has_calls(calls)

    def test_matches_pattern_list_true(self):
        test_pattern_list = [re.compile("PATTERN1"), re.compile("PATTERN2")]
        test_name = "testsnap_PATTERN2"
        result = self._action.matches_pattern_list(test_name, test_pattern_list)
        self.assertEqual(result, True)

    def test_matches_pattern_list_false(self):
        test_pattern_list = [re.compile("PATTERN1"), re.compile("PATTERN2")]
        test_name = "testsnap"
        result = self._action.matches_pattern_list(test_name, test_pattern_list)
        self.assertEqual(result, False)

    @mock.patch('vm_snapshots_delete.datetime')
    @mock.patch('vmwarelib.inventory.get_virtualmachines')
    def test_delete_old_snapshots(self, mock_inventory, mock_datetime):
        # Define test variables
        test_max_age_days = 2
        test_name_ignore_regexes = [re.compile("^.*IGNORE$")]

        # Mock 3 snapshot objects and make one of them a child
        mock_snap1 = mock.MagicMock(createTime=1)
        type(mock_snap1).name = mock.PropertyMock(return_value="snap1")
        mock_snap1.vm.name = "vm1"
        mock_snap1.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_snap2 = mock.MagicMock(createTime=1)
        type(mock_snap2).name = mock.PropertyMock(return_value="snap2")
        mock_snap2.vm.name = "vm2"
        mock_snap2.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_child_snap = mock.MagicMock(createTime=1)
        type(mock_child_snap).name = mock.PropertyMock(return_value="ignore_snap IGNORE")
        mock_child_snap.vm.name = "vm3"
        mock_child_snap.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_snap2.childSnapshotList = [mock_child_snap]

        mock_datetime.datetime.utcnow().replace.return_value = 3
        mock_datetime.timedelta.return_value = 1

        # Mock a list of 3 "snapshots"
        test_snap_list = [mock_snap1, mock_snap2]

        expected_result = {'deleted_snapshots': ["vm1: snap1", "vm2: snap2"],
                           'ignored_snapshots': ["vm3: ignore_snap IGNORE"]}

        # Run function and verify results
        result = self._action.delete_old_snapshots(test_snap_list,
                                                   test_max_age_days,
                                                   test_name_ignore_regexes)

        self.assertEqual(result, expected_result)
        mock_datetime.timedelta.assert_called_with(days=test_max_age_days)
        mock_snap1.snapshot.RemoveSnapshot_Task.assert_called_with(removeChildren=False,
                                                                   consolidate=True)
        mock_snap2.snapshot.RemoveSnapshot_Task.assert_called_with(removeChildren=False,
                                                                   consolidate=True)

    @mock.patch('vm_snapshots_delete.datetime')
    @mock.patch('vmwarelib.inventory.get_virtualmachines')
    def test_delete_old_snapshots_encoding(self, mock_inventory, mock_datetime):
        # Define test variables
        test_max_age_days = 2
        test_name_ignore_regexes = [re.compile("^.*IGNORE$")]

        # Mock 3 snapshot objects and make one of them a child
        mock_snap1 = mock.MagicMock(createTime=1)
        type(mock_snap1).name = mock.PropertyMock(return_value="VM Snapshot 11%252f13%252f2019")
        mock_snap1.vm.name = "vm1"
        mock_snap1.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_snap2 = mock.MagicMock(createTime=1)
        type(mock_snap2).name = mock.PropertyMock(return_value="snap2")
        mock_snap2.vm.name = "vm2"
        mock_snap2.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_child_snap = mock.MagicMock(createTime=1)
        child_snap_name = "VM Snapshot 11%252f1325%252f2019 IGNORE"
        type(mock_child_snap).name = mock.PropertyMock(return_value=child_snap_name)
        mock_child_snap.vm.name = "vm3"
        mock_child_snap.snapshot.RemoveSnapshot_Task.return_value = "test"

        mock_snap2.childSnapshotList = [mock_child_snap]

        mock_datetime.datetime.utcnow().replace.return_value = 3
        mock_datetime.timedelta.return_value = 1

        # Mock a list of 3 "snapshots"
        test_snap_list = [mock_snap1, mock_snap2]

        expected_result = {'deleted_snapshots': ["vm1: VM Snapshot 11%252f13%252f2019",
                                                 "vm2: snap2"],
                           'ignored_snapshots': ["vm3: VM Snapshot 11%252f1325%252f2019 IGNORE"]}

        # Run function and verify results
        result = self._action.delete_old_snapshots(test_snap_list,
                                                   test_max_age_days,
                                                   test_name_ignore_regexes)

        self.assertEqual(result, expected_result)
        mock_datetime.timedelta.assert_called_with(days=test_max_age_days)
        mock_snap1.snapshot.RemoveSnapshot_Task.assert_called_with(removeChildren=False,
                                                                   consolidate=True)
        mock_snap2.snapshot.RemoveSnapshot_Task.assert_called_with(removeChildren=False,
                                                                   consolidate=True)

    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.delete_old_snapshots')
    @mock.patch('vmwarelib.inventory.get_virtualmachines')
    def test_delete_all_old_snapshots(self, mock_inventory, mock_delete):
        # Define test variables
        test_max_age_days = 2
        test_name_ignore_regexes = ["^.*IGNORE$"]

        expected_result = {'deleted_snapshots': ["snap1", "snap2"],
                           'ignored_snapshots': []}

        # Mock function results
        mock_vm1 = mock.MagicMock()
        mock_vm1.snapshot.rootSnapshotList = ["snap1"]

        mock_vm2 = mock.MagicMock()
        mock_vm2.snapshot.rootSnapshotList = ["snap2"]

        # Mock a list of 2 VMs with "snapshots" and one without
        test_vm_list = ["vm_no_snaps", mock_vm1, mock_vm2]
        mock_vm_list = mock.MagicMock(view=test_vm_list)
        mock_inventory.return_value = mock_vm_list

        side_effect = [{'deleted_snapshots': ["snap1"], 'ignored_snapshots': []},
                       {'deleted_snapshots': ["snap2"], 'ignored_snapshots': []}]
        mock_delete.side_effect = side_effect

        # Run function and verify results
        result = self._action.delete_all_old_snapshots(test_max_age_days, test_name_ignore_regexes)

        self.assertEqual(result, expected_result)
        mock_inventory.assert_called_with(self._action.si_content)

        calls = [mock.call(["snap1"], test_max_age_days, test_name_ignore_regexes),
                 mock.call(["snap2"], test_max_age_days, test_name_ignore_regexes)]
        mock_delete.assert_has_calls(calls)

    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.compile_regexes')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run_invalid_name(self, mock_inventory, mock_compile_regexes):
        # Define test variables
        test_vsphere = "vsphere"
        test_max_age_days = 2
        test_name_ignore_regexes = ["^.*IGNORE$"]
        test_vm_name = "testvm"
        test_patterns = "test_patterns"

        # Mock function results
        mock_compile_regexes.return_value = test_patterns

        # invoke action with invalid names which don't match any objects
        mock_inventory.side_effect = Exception("Inventory Error: Unable to Find Object in a test")
        with self.assertRaises(Exception):
            self._action.run(max_age_days=test_max_age_days,
                             name_ignore_regexes=test_name_ignore_regexes,
                             vm_id=None,
                             vm_name=test_vm_name,
                             vsphere=test_vsphere)
            mock_inventory.assert_called_with(self._action.si_content, moid=None, name=test_vm_name)
            mock_compile_regexes.assert_called_with(test_name_ignore_regexes)

    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.compile_regexes')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run_no_snaps(self, mock_inventory, mock_compile_regexes):
        # Define test variables
        test_vsphere = "vsphere"
        test_max_age_days = 2
        test_name_ignore_regexes = ["^.*IGNORE$"]
        test_vm_name = "testvm"
        test_patterns = "test_patterns"

        # Mock function results
        mock_compile_regexes.return_value = test_patterns

        mock_vm = mock.Mock()
        mock_inventory.return_value = mock_vm
        type(mock_vm).name = mock.PropertyMock(return_value=test_vm_name)
        type(mock_vm).snapshot = mock.PropertyMock(side_effect=ValueError)

        # Run function and verify results
        result = self._action.run(max_age_days=test_max_age_days,
                                  name_ignore_regexes=test_name_ignore_regexes,
                                  vm_id=None,
                                  vm_name=test_vm_name,
                                  vsphere=test_vsphere)

        self.assertEqual(result, "No snapshots found for VM: testvm")
        mock_inventory.assert_called_with(self._action.si_content, moid=None, name=test_vm_name)
        mock_compile_regexes.assert_called_with(test_name_ignore_regexes)

    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.compile_regexes')
    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.delete_all_old_snapshots')
    def test_run_all_snaps(self, mock_delete_all_snaps, mock_compile_regexes):
        # Define test variables
        test_vsphere = "vsphere"
        test_max_age_days = 2
        test_name_ignore_regexes = ["^.*IGNORE$"]
        test_patterns = "test_patterns"

        # Mock function results
        mock_compile_regexes.return_value = test_patterns

        expected_result = "result"
        mock_delete_all_snaps.return_value = expected_result

        # Run function and verify results
        result = self._action.run(max_age_days=test_max_age_days,
                                  name_ignore_regexes=test_name_ignore_regexes,
                                  vm_id=None,
                                  vm_name=None,
                                  vsphere=test_vsphere)

        self.assertEqual(result, expected_result)
        mock_compile_regexes.assert_called_with(test_name_ignore_regexes)
        mock_delete_all_snaps.assert_called_with(test_max_age_days, test_patterns)

    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.compile_regexes')
    @mock.patch('vm_snapshots_delete.VMSnapshotsDelete.delete_old_snapshots')
    @mock.patch('vmwarelib.inventory.get_virtualmachine')
    def test_run(self, mock_inventory, mock_delete_snaps, mock_compile_regexes):
        # Define test variables
        test_vsphere = "vsphere"
        test_max_age_days = 2
        test_name_ignore_regexes = ["^.*IGNORE$"]
        test_vm_name = "testvm"
        test_patterns = "test_patterns"
        test_snap_list = ["test_list"]

        # Mock function results
        mock_compile_regexes.return_value = test_patterns

        expected_result = "result"
        mock_delete_snaps.return_value = expected_result

        mock_vm = mock.MagicMock()
        mock_inventory.return_value = mock_vm

        mock_vm.snapshot.rootSnapshotList = test_snap_list

        # Run function and verify results
        result = self._action.run(max_age_days=test_max_age_days,
                                  name_ignore_regexes=test_name_ignore_regexes,
                                  vm_id=None,
                                  vm_name=test_vm_name,
                                  vsphere=test_vsphere)

        self.assertEqual(result, expected_result)
        mock_inventory.assert_called_with(self._action.si_content, moid=None, name=test_vm_name)
        mock_delete_snaps.assert_called_with(test_snap_list, test_max_age_days, test_patterns)
        mock_compile_regexes.assert_called_with(test_name_ignore_regexes)
