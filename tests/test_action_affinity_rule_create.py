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
from affinity_rule_create import AffinityRuleCreate
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'AffinityRuleCreate'
]


class AffinityRuleCreateTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = AffinityRuleCreate

    def setUp(self):
        super(AffinityRuleCreateTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch("affinity_rule_create.vim")
    def test_create_group_vm(self, mock_vim):
        test_dict = {
            'rule_name': 'test_rule',
            'object_array': ['vm1'],
            'group_type': 'vm'
        }
        expected_group_name = "{0}-vm".format(test_dict['rule_name'])
        expected_result = "Expected Return"

        mock_vim.cluster.VmGroup.return_value = "VM Group Return"
        mock_vim.cluster.GroupSpec.return_value = expected_result

        result_value_name, result_value_spec = self._action.create_group(**test_dict)
        self.assertEqual(result_value_name, expected_group_name)
        self.assertEqual(result_value_spec, expected_result)

    @mock.patch("affinity_rule_create.vim")
    def test_create_group_host(self, mock_vim):
        test_dict = {
            'rule_name': 'test_rule',
            'object_array': ['host1'],
            'group_type': 'host'
        }
        expected_group_name = "{0}-host".format(test_dict['rule_name'])
        expected_result = "Expected Return"

        mock_vim.cluster.HostGroup.return_value = "Host Group Return"
        mock_vim.cluster.GroupSpec.return_value = expected_result

        result_value_name, result_value_spec = self._action.create_group(**test_dict)
        self.assertEqual(result_value_name, expected_group_name)
        self.assertEqual(result_value_spec, expected_result)

    @mock.patch("affinity_rule_create.vim")
    def test_create_group_error(self, mock_vim):
        test_dict = {
            'rule_name': 'test_rule',
            'object_array': ['host1'],
            'group_type': 'storage'
        }
        expected_result = "Expected Return"

        mock_vim.cluster.HostGroup.return_value = "Host Group Return"
        mock_vim.cluster.GroupSpec.return_value = expected_result

        with self.assertRaises(ValueError):
            self._action.create_group(**test_dict)

    @mock.patch("affinity_rule_create.vim")
    def test_create_rule(self, mock_vim):
        test_dict = {
            'rule_name': 'test_rule',
            'vm_group': 'vm_group',
            'host_group': 'host_group'
        }
        expected_result = "Expected Return"

        mock_vim.cluster.VmHostRuleInfo.return_value = "Rule Return"
        mock_vim.cluster.RuleSpec.return_value = expected_result

        result_value = self._action.create_rule(**test_dict)
        self.assertEqual(result_value, expected_result)

    def test_wait_for_vm(self):
        test_dict = {
            'vm_name': 'test_vm',
            'vm_wait_retry': 1
        }

        mock_vm = mock.Mock()
        vm_name_property = mock.PropertyMock(return_value=test_dict['vm_name'])
        type(mock_vm).name = vm_name_property
        mock_view = mock.Mock(view=[mock_vm])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        result_value = self._action.wait_for_vm(**test_dict)
        self.assertEqual(result_value, mock_vm)

    def test_wait_for_vm_error(self):
        test_dict = {
            'vm_name': 'test_vm',
            'vm_wait_retry': 1
        }

        mock_vm = None
        mock_view = mock.Mock(view=[mock_vm])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        with self.assertRaises(ValueError):
            self._action.wait_for_vm(**test_dict)

    @mock.patch("affinity_rule_create.vim")
    @mock.patch("vmwarelib.actions.BaseAction._wait_for_task")
    def test_run(self, mock__wait_for_task, mock_vim):
        test_dict = {
            'rule_name': 'test_rule',
            'cluster_name': 'test_cluster',
            'vm_names': ['test_vm'],
            'vm_wait_retry': 1
        }

        mock_cluster = mock.Mock()
        mock_cluster.ReconfigureEx.return_value = "Cluster Reconfigure Return"
        cluster_name_property = mock.PropertyMock(return_value=test_dict['cluster_name'])
        type(mock_cluster).name = cluster_name_property

        mock_host = mock.Mock()
        host_name_property = mock.PropertyMock(return_value="test_host")
        type(mock_host).name = host_name_property

        mock_vm = mock.Mock()
        mock_vm.runtime.host = mock_host
        vm_name_property = mock.PropertyMock(return_value=test_dict['vm_names'][0])
        type(mock_vm).name = vm_name_property

        mock_view = mock.Mock(view=[mock_vm, mock_cluster])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        mock_vim.cluster.ConfigSpecEx.result_value = "Return Config"
        mock__wait_for_task.return_value = True

        result_value = self._action.run(**test_dict)
        self.assertEqual(result_value, (True, {'host_names': ["test_host"]}))
