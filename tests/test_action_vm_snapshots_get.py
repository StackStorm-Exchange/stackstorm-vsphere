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
from vm_snapshots_get import VMSnapshotsGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'VMSnapshotsGetTestCase'
]


class VMSnapshotsGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMSnapshotsGet

    def generate_mock_vm(self):
        mock_vm = mock.MagicMock()
        mock_disk1 = mock.MagicMock()
        type(mock_disk1).name = 'whatever'
        type(mock_disk1).type = 'snapshotData'
        type(mock_disk1).size = 1073741824
        mock_disk2 = mock.MagicMock()
        type(mock_disk2).name = 'this_is_not_a_snapshot_disk'
        type(mock_disk2).type = 'whatever'
        type(mock_disk2).size = 2147483648
        mock_disk3 = mock.MagicMock()
        type(mock_disk3).name = '000096-this_is_a_snapshot_disk'
        type(mock_disk3).type = 'whatever'
        type(mock_disk3).size = 4294967296
        mock_vm.layoutEx.file = [mock_disk1, mock_disk2, mock_disk3]

        return mock_vm

    def generate_mock_snapshots(self):
        mock_snap1 = mock.MagicMock()
        type(mock_snap1).name = "snap_name"
        type(mock_snap1).description = "snap_description"
        type(mock_snap1).id = 100
        type(mock_snap1).createTime = "january"
        type(mock_snap1).vm = "whatever:vm-10"
        type(mock_snap1).snapshot = "whatever:snapshot-1000"
        type(mock_snap1).state = "poweredOn"
        mock_snap2 = mock.MagicMock()
        type(mock_snap2).name = "snap_name2"
        type(mock_snap2).description = "snap_description2"
        type(mock_snap2).id = 101
        type(mock_snap2).createTime = "february"
        type(mock_snap2).vm = "whatever:vm-11"
        type(mock_snap2).snapshot = "whatever:snapshot-1001"
        type(mock_snap2).state = "poweredOff"

        type(mock_snap1).childSnapshotList = [mock_snap2]
        type(mock_snap2).childSnapshotList = []

        return [mock_snap1]

    def test_get_snapshots_size_gb(self):
        self._action = self.get_action_instance(self.new_config)
        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

        mock_vm = self.generate_mock_vm()

        result = self._action.get_snapshots_size_gb(mock_vm)

        expected_result = 5.0
        self.assertEqual(result, expected_result)

    def test_get_snapshots_details_flat(self):
        self._action = self.get_action_instance(self.new_config)
        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

        mock_snap = self.generate_mock_snapshots()

        result = self._action.get_snapshots_details(mock_snap, True)

        expected_result = [{"name": "snap_name",
                            "created": "january",
                            "snapshot_moid": "snapshot-1000",
                            "state": "poweredOn",
                            "vm_moid": "vm-10",
                            "id": 100,
                            "description": "snap_description"},
                           {"name": "snap_name2",
                            "created": "february",
                            "snapshot_moid": "snapshot-1001",
                            "state": "poweredOff",
                            "vm_moid": "vm-11",
                            "id": 101,
                            "description": "snap_description2"}]
        self.assertEqual(result, expected_result)

    def test_get_snapshots_details_tree(self):
        self._action = self.get_action_instance(self.new_config)
        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

        mock_snap = self.generate_mock_snapshots()

        result = self._action.get_snapshots_details(mock_snap, False)

        expected_result = [{"name": "snap_name",
                            "created": "january",
                            "snapshot_moid": "snapshot-1000",
                            "state": "poweredOn",
                            "vm_moid": "vm-10",
                            "id": 100,
                            "description": "snap_description",
                            "child_snapshots": [{"name": "snap_name2",
                                                 "created": "february",
                                                 "snapshot_moid": "snapshot-1001",
                                                 "state": "poweredOff",
                                                 "vm_moid": "vm-11",
                                                 "id": 101,
                                                 "description": "snap_description2"}]}]
        self.assertEqual(result, expected_result)
