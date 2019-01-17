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
from affinity_rule_delete import AffinityRuleDelete
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'AffinityRuleDelete'
]


class AffinityRuleDeleteTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = AffinityRuleDelete

    def setUp(self):
        super(AffinityRuleDeleteTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_find_affinity_groups(self):
        expected_vm_group_name = "Test_vm"
        mock_vm = mock.Mock()
        vm_name_property = mock.PropertyMock(return_value=expected_vm_group_name)
        type(mock_vm).name = vm_name_property

        expected_host_group_name = "Test_host"
        mock_host = mock.Mock()
        mock_host_property = mock.PropertyMock(return_value=expected_host_group_name)
        type(mock_host).name = mock_host_property

        mock_cluster = mock.Mock()
        mock_config_group = mock.Mock(group=[mock_vm, mock_host])
        mock_cluster = mock.Mock(configurationEx=mock_config_group)

        test_dict = {
            'cluster': mock_cluster,
            'vm_group_name': expected_vm_group_name,
            'host_group_name': expected_host_group_name
        }

        result_value_vm, result_value_host = self._action.find_affinity_groups(**test_dict)
        self.assertEqual(result_value_vm, mock_vm)
        self.assertEqual(result_value_host, mock_host)

    def test_find_affinity_groups_vm_error(self):
        expected_vm_group_name = "Test_vm"
        expected_host_group_name = "Test_host"
        mock_host = mock.Mock()
        mock_host_property = mock.PropertyMock(return_value=expected_host_group_name)
        type(mock_host).name = mock_host_property

        mock_cluster = mock.Mock()
        mock_config_group = mock.Mock(group=[mock_host])
        mock_cluster = mock.Mock(configurationEx=mock_config_group)

        test_dict = {
            'cluster': mock_cluster,
            'vm_group_name': expected_vm_group_name,
            'host_group_name': expected_host_group_name
        }

        with self.assertRaises(ValueError):
            self._action.find_affinity_groups(**test_dict)

    def test_find_affinity_groups_host_error(self):
        expected_host_group_name = "Test_host"
        expected_vm_group_name = "Test_vm"
        mock_vm = mock.Mock()
        vm_name_property = mock.PropertyMock(return_value=expected_vm_group_name)
        type(mock_vm).name = vm_name_property

        mock_cluster = mock.Mock()
        mock_config_group = mock.Mock(group=[mock_vm])
        mock_cluster = mock.Mock(configurationEx=mock_config_group)

        test_dict = {
            'cluster': mock_cluster,
            'vm_group_name': expected_vm_group_name,
            'host_group_name': expected_host_group_name
        }

        with self.assertRaises(ValueError):
            self._action.find_affinity_groups(**test_dict)

    def test_find_affinity_rule(self):
        rule_name = "Test_Rule"

        mock_rule = mock.Mock(key="1")
        rule_name_property = mock.PropertyMock(return_value=rule_name)
        type(mock_rule).name = rule_name_property

        mock_config_rule = mock.Mock(rule=[mock_rule])
        mock_cluster = mock.Mock(configurationEx=mock_config_rule)

        test_dict = {
            'cluster': mock_cluster,
            'rule_name': rule_name
        }

        result_value = self._action.find_affinity_rule(**test_dict)
        self.assertEqual(result_value, mock_rule)

    def test_find_affinity_rule_error(self):
        rule_name = "Test_Rule"

        mock_rule = mock.Mock(key="1")
        rule_name_property = mock.PropertyMock(return_value="stackstorm-error")
        type(mock_rule).name = rule_name_property

        mock_config_rule = mock.Mock(rule=[mock_rule])
        mock_cluster = mock.Mock(configurationEx=mock_config_rule)

        test_dict = {
            'cluster': mock_cluster,
            'rule_name': rule_name
        }

        with self.assertRaises(ValueError):
            self._action.find_affinity_rule(**test_dict)

    @mock.patch("affinity_rule_delete.vim")
    def test_build_cluster_removal_spec(self, mock_vim):

        expected_vm_group_name = "Test_vm"
        mock_vm = mock.Mock()
        vm_name_property = mock.PropertyMock(return_value=expected_vm_group_name)
        type(mock_vm).name = vm_name_property

        expected_host_group_name = "Test_host"
        mock_host = mock.Mock()
        mock_host_property = mock.PropertyMock(return_value=expected_host_group_name)
        type(mock_host).name = mock_host_property

        mock_rule = mock.Mock(key="1")
        rule_name_property = mock.PropertyMock(return_value="stackstorm-vm_test")
        type(mock_rule).name = rule_name_property

        test_dict = {
            'affinity_rule': mock_rule,
            'vm_group': mock_vm,
            'host_group': mock_host
        }
        expected_result = "Config Spec Return"

        mock_vim.cluster.GroupSpec.side_effect = ["VM Group Return", "Host Group Return"]
        mock_vim.cluster.RuleSpec.return_value = "Rule Spec Return"
        mock_vim.cluster.ConfigSpecEx.return_value = expected_result

        result_value = self._action.build_cluster_removal_spec(**test_dict)
        self.assertEqual(result_value, expected_result)

    @mock.patch("affinity_rule_delete.AffinityRuleDelete.find_affinity_groups")
    @mock.patch("affinity_rule_delete.AffinityRuleDelete.find_affinity_rule")
    @mock.patch("affinity_rule_delete.vim")
    @mock.patch("vmwarelib.actions.BaseAction._wait_for_task")
    def test_run(self,
                mock__wait_for_task,
                mock_vim,
                mock_find_affinity_rule,
                mock_find_affinity_groups):
        test_dict = {
            'rule_name': 'test_rule',
            'cluster_name': 'test_cluster'
        }

        expected_vm_group_name = "Test_vm_group"
        mock_vm_group = mock.Mock()
        vm_name_group_property = mock.PropertyMock(return_value=expected_vm_group_name)
        type(mock_vm_group).name = vm_name_group_property

        expected_host_group_name = "Test_host_group"
        mock_host_group = mock.Mock()
        mock_host_group_property = mock.PropertyMock(return_value=expected_host_group_name)
        type(mock_host_group).name = mock_host_group_property

        mock_rule = mock.Mock(key="1")
        rule_name = test_dict['rule_name']
        rule_name_property = mock.PropertyMock(return_value=rule_name)
        type(mock_rule).name = rule_name_property
        mock_rule.vmGroupName.return_value = expected_vm_group_name
        mock_rule.affineHostGroupName.return_value = expected_host_group_name

        mock_find_affinity_rule.return_value = mock_rule
        mock_find_affinity_groups.return_value = (mock_vm_group, mock_host_group)

        mock_config_rule = mock.Mock(rule=[mock_rule])
        mock_cluster = mock.Mock(configurationEx=mock_config_rule)
        mock_cluster.ReconfigureEx.return_value = "Cluster Reconfigure Return"
        cluster_name_property = mock.PropertyMock(return_value=test_dict['cluster_name'])
        type(mock_cluster).name = cluster_name_property
        mock_view = mock.Mock(view=[mock_cluster])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        mock_vim.cluster.GroupSpec.side_effect = ["VM Group Return", "Host Group Return"]
        mock_vim.cluster.RuleSpec.return_value = "Rule Spec Return"
        mock_vim.cluster.ConfigSpecEx.return_value = "Config Spec Return"

        mock__wait_for_task.return_value = True

        result_value = self._action.run(**test_dict)
        self.assertEqual(result_value, True)
