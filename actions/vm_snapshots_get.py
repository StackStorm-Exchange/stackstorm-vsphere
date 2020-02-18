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

from vmwarelib.actions import BaseAction
from vmwarelib import inventory
import re


class VMSnapshotsGet(BaseAction):
    def run(self, vm_id, vm_name, vsphere=None):
        """
        Display snapshots

        Args:
        - vm_id: Moid of Virtual Machine to retrieve
        - vm_name: Name of Virtual Machine to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: Total snapshots size
        - dict: Lists of snapshots found
        """
        self.establish_connection(vsphere)

        # If a VM ID or name was given then only remove snapshots from that VM
        if vm_id or vm_name:
            vm = inventory.get_virtualmachine(self.si_content, moid=vm_id, name=vm_name)

            # Check if any snapshots exist on the VM
            try:
                snapshots = vm.snapshot.rootSnapshotList
            except:
                return "No snapshots found for VM: {}".format(vm.name)

            retval = {}
            retval["size_gb"] = self.get_snapshot_size(vm)
            retval["snapshots"] = []

            while snapshots:
                for s in snapshots:
                    snap = {}
                    snap["name"] = s.name.encode('utf-8')
                    snap["description"] = s.description.encode('utf-8')
                    snap["id"] = s.id
                    snap["created"] = str(s.createTime)
                    snap["vm"] = str(s.vm).encode('utf-8').split(':')[-1]
                    snap["snapshot"] = str(s.snapshot).encode('utf-8').split(':')[-1]
                    snap["state"] = s.state.encode('utf-8')

                    retval["snapshots"].append(snap)

                    if s.childSnapshotList:
                        snapshots = s.childSnapshotList
                    else:
                        snapshots = []

            return retval

    def get_snapshot_size(self, vsphere_vm):
        """returns snapshot size, in GB for a VM"""
        disk_list = vsphere_vm.layoutEx.file
        size = 0
        for disk in disk_list:
            if disk.type == 'snapshotData':
                size += disk.size
            ss_disk = re.search('0000\d\d',disk.name)
            if ss_disk:
                size += disk.size

        size_gb = (float(size) / 1024 / 1024 / 1024)
        return round(size_gb, 2)
