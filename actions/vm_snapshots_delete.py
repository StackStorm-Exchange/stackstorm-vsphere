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
import datetime
import pytz


class VMSnapshotsDelete(BaseAction):
    def delete_old_snapshots(self, snapshot_list, max_age_days, name_ignore_patterns):
        """Deletes all snapshots from the given list that are older than max_age_days.
        Ignorning any snapshot with a name that matches one of the name_ignore_pattern.
        """
        date_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        deleted_snapshots = []
        ignored_snapshots = []

        for snap in snapshot_list:
            # remove_date is the date the snapshot was created plus max_age_days
            # Any snapshots older than remove_date will be deleted unless its name includes
            # an item from name_ignore_patterns
            remove_date = snap.createTime + datetime.timedelta(days=max_age_days)

            # we need to encode snap shot names because
            # VM Snapshot 11/13/2019, 9:59:56 AM -> VM Snapshot 11%252f13%252f2019, 9:59:56 AM
            snap_name = snap.name.encode('utf-8')

            # ignore if the snapshot name matches one of the regexes
            if self.matches_pattern_list(snap_name, name_ignore_patterns):
                ignored_snapshots.append("{0}: {1}".format(snap.vm.name, snap_name))

            # Snapshots older than the max age will be deleted
            elif remove_date < date_now:
                deleted_snapshots.append("{0}: {1}".format(snap.vm.name, snap_name))
                snap.snapshot.RemoveSnapshot_Task(removeChildren=False, consolidate=True)

            # Re-run this function with the child snapshot list of any children are found
            if snap.childSnapshotList:
                child_result = self.delete_old_snapshots(snap.childSnapshotList,
                                                         max_age_days,
                                                         name_ignore_patterns)

                # Append the results from the child snapshots
                deleted_snapshots += child_result['deleted_snapshots']
                ignored_snapshots += child_result['ignored_snapshots']

        return {'deleted_snapshots': deleted_snapshots,
                'ignored_snapshots': ignored_snapshots}

    def delete_all_old_snapshots(self, max_age_days, name_ignore_patterns):
        """Deletes all snapshots from all VMs that are older than max_age_days.
        Ignorning any snapshot with a name that matches one of the name_ignore_pattern.
        """
        # Retrieve a list of all VMs in vSphere
        vm_list = inventory.get_virtualmachines(self.si_content)
        deleted_snapshots = []
        ignored_snapshots = []
        for vm in vm_list.view:
            # Check if any snapshots exist on the VM
            try:
                snapshots = vm.snapshot.rootSnapshotList
            except Exception as e:
                print(f'No snapshots found for VM. {e}')

            result = self.delete_old_snapshots(snapshots, max_age_days, name_ignore_patterns)
            # Append the results from each VM
            deleted_snapshots += result['deleted_snapshots']
            ignored_snapshots += result['ignored_snapshots']

        return {'deleted_snapshots': deleted_snapshots,
                'ignored_snapshots': ignored_snapshots}

    def compile_regexes(self, regex_list):
        """Compiles all of the regexes in the list into patterns
        :returns: list of compiled patterns
        """
        patterns = []
        for r in regex_list:
            patterns.append(re.compile(r))
        return patterns

    def matches_pattern_list(self, name, pattern_list):
        """Compares the name to each pattern in the list
        :returns: True if the name matches any of the patterns. False if nothing matches.
        """
        for p in pattern_list:
            if p.search(name):
                return True
        return False

    def run(self, max_age_days, name_ignore_regexes, vm_id, vm_name, vsphere=None):
        """
        Deletes all snapshots that are older than max_age_days on either all VMs or the given VM.
        Ignore any snapshot with a name that matches one of the name_ignore_regexes.

        Args:
        - max_age_days: Number of days that a snapshot will exist before getting deleted
        - name_ignore_regexes: Compares the snapshot name to the regex. If matched, the snapshot
            will be ignored and NOT deleted
        - vm_id: Moid of Virtual Machine to retrieve
        - vm_name: Name of Virtual Machine to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: Lists of snapshots that were deleted and ignored
        """
        self.establish_connection(vsphere)

        ignore_patterns = self.compile_regexes(name_ignore_regexes)

        # If a VM ID or name was given then only remove snapshots from that VM
        if vm_id or vm_name:
            vm = inventory.get_virtualmachine(self.si_content, moid=vm_id, name=vm_name)

            # Check if any snapshots exist on the VM
            try:
                snapshots = vm.snapshot.rootSnapshotList
            except:
                return "No snapshots found for VM: {}".format(vm.name)

            return self.delete_old_snapshots(snapshots, max_age_days, ignore_patterns)
        # If no VM was given then remove snapshots from all VMs
        else:
            return self.delete_all_old_snapshots(max_age_days, ignore_patterns)
