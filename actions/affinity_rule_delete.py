# Disable message for: No name 'vim' in module 'pyVmomi' (no-name-in-module)
from pyVmomi import vim  # pylint: disable-msg=no-name-in-module
from vmwarelib.actions import BaseAction
from vmwarelib import inventory


class VmwareAffinityRuleDelete(BaseAction):

    def run(self, rule_name, cluster_name, vsphere=None):
        """Main entry point for the StackStorm actions to execute the operation.
        :returns: boolean
        """
        # Connect to the vCenter
        self.establish_connection(vsphere)

        # Finds cluster by name
        cluster = inventory.get_cluster(self.si_content, name=cluster_name)

        # Get the associated affinity rule
        affinity_rule = self.find_affinity_rule(rule_name, cluster)

        # Find the groups from the affinity rule since it just returns the name
        vm_group, host_group = self.find_affinity_groups(cluster,
                                                        affinity_rule.vmGroupName,
                                                        affinity_rule.affineHostGroupName)

        # Create cluster change config to be passed to vmware
        config_spec = self.build_cluster_removal_spec(affinity_rule, vm_group, host_group)

        # Run Reconfigure task
        task_return = self._wait_for_task(cluster.ReconfigureEx(config_spec, modify=True))

        return task_return

    def find_affinity_groups(self, cluster, vm_group_name, host_group_name):
        """Finds the host and vm groups that would be associated with
        the affinity rule that we are trying to remove.
        """
        vm_group = None
        host_group = None

        for group in cluster.configurationEx.group:
            if group.name == vm_group_name:
                vm_group = group
            elif group.name == host_group_name:
                host_group = group

            if vm_group and host_group:
                break

        if not vm_group:
            raise ValueError("Could not find VM Group with the name: {0}".format(vm_group_name))

        if not host_group:
            raise ValueError(("Could not find Host Group with the name: {0}"
                            "".format(host_group_name)))

        return (vm_group, host_group)

    def find_affinity_rule(self, rule_name, cluster):
        """ Finds the affinity rule that for the specific rule name
        """

        affinity_rule = None
        for rule in cluster.configurationEx.rule:
            if rule.name == rule_name:
                affinity_rule = rule
                break

        if not affinity_rule:
            raise ValueError("Could not find Affinity Rule with the name: {0}".format(rule_name))

        return affinity_rule

    def build_cluster_removal_spec(self, affinity_rule, vm_group, host_group):
        """ Build the removal spec to be passed in to the cluster so that
        vmware removes the affinity rule and the groups from the cluster
        """
        # For remove operation a removeKey is required
        vm_group_spec = vim.cluster.GroupSpec(info=vm_group,
                                             operation='remove',
                                             removeKey=vm_group.name)
        host_group_spec = vim.cluster.GroupSpec(info=host_group,
                                               operation='remove',
                                               removeKey=host_group.name)
        affinity_rule_spec = vim.cluster.RuleSpec(info=affinity_rule,
                                                 operation='remove',
                                                 removeKey=affinity_rule.key)

        config_spec = vim.cluster.ConfigSpecEx(groupSpec=[vm_group_spec, host_group_spec],
                                              rulesSpec=[affinity_rule_spec])

        return config_spec
