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

# Disable message for: No name 'vim' in module 'pyVmomi' (no-name-in-module)
from pyVmomi import vim  # pylint: disable-msg=no-name-in-module
import time


class AffinityRuleCreate(BaseAction):

    def run(self, vm_names, vm_wait_retry, rule_name, cluster_name, host_names=None, vsphere=None):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: boolean
        """
        # Connect to the vCenter
        self.establish_connection(vsphere)

        # Find the vm to add to the affinity rule
        vms = []
        for vm_name in vm_names:
            vms.append(self.wait_for_vm(vm_name, vm_wait_retry))

        hosts = []
        if host_names:
            for host_name in host_names:
                hosts.append(inventory.get_hostsystem(self.si_content, name=host_name))
        else:
            for vm in vms:
                # Get the host that the vm is current on
                hosts.append(vm.runtime.host)

        # Finds cluster by name
        cluster = inventory.get_cluster(self.si_content, name=cluster_name)

        # Create Affinity groups
        vm_group_name, vm_group_spec = self.create_group(rule_name, vms, "vm")
        host_group_name, host_group_spec = self.create_group(rule_name, hosts, "host")

        # Create Affinity rules
        affinity_rule_spec = self.create_rule(rule_name, vm_group_name, host_group_name)

        # Create cluster change config to be passed to vmware
        config_spec = vim.cluster.ConfigSpecEx(groupSpec=[vm_group_spec, host_group_spec],
                                               rulesSpec=[affinity_rule_spec])

        # Run Reconfigure task
        task_return = self._wait_for_task(cluster.ReconfigureEx(config_spec, modify=True))

        host_name_return = []
        for host in hosts:
            host_name_return.append(host.name)

        return (task_return, {'host_names': host_name_return})

    def create_group(self, rule_name, object_array, group_type):
        """ Creates a group to be created in VMware. Returns the group
        name and spec to be used later. We support vm and host groups.
        """
        group_name = ""
        group_object = None
        if group_type == "vm":
            group_name = "{0}-vm".format(rule_name)
            group_object = vim.cluster.VmGroup(name=group_name, vm=object_array)
        elif group_type == "host":
            group_name = "{0}-host".format(rule_name)
            group_object = vim.cluster.HostGroup(name=group_name, host=object_array)
        else:
            raise ValueError(("Must choose either vm or host as the group type."
                              "Type supplied: {0}".format(group_type)))

        group_spec = vim.cluster.GroupSpec(info=group_object, operation='add')

        return (group_name, group_spec)

    def create_rule(self, rule_name, vm_group, host_group):
        """ Creates an affinity rule spec to be passed into the
        Cluster reconfigure spec for vmware.
        """
        rule_obj = vim.cluster.VmHostRuleInfo(vmGroupName=vm_group,
                                              affineHostGroupName=host_group,
                                              name=rule_name,
                                              enabled=True,
                                              mandatory=True)
        rule_spec = vim.cluster.RuleSpec(info=rule_obj, operation='add')

        return rule_spec

    def wait_for_vm(self, vm_name, vm_wait_retry):
        """ The VM object has to exist before it can be added to the affinity
        rule. Since we will can kick off this method at the same time as a
        provision we may need to wait for the vm to be created.
        """
        vm = None
        count = 0
        while count < vm_wait_retry:
            try:
                vm = inventory.get_virtualmachine(self.si_content, name=vm_name)
                break
            except Exception:
                count += 1
                time.sleep(2)

        if not vm:
            raise ValueError("Could not find Virtual Machine with name: {0}".format(vm_name))

        return vm
