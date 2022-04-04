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

import json
import mock
import yaml

from st2tests.base import BaseActionTestCase


class VsphereBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(VsphereBaseActionTestCase, self).setUp()

        self._blank_config = self.load_yaml('cfg_blank.yaml')
        self._old_config = self.load_yaml('cfg_old.yaml')
        self._new_config = self.load_yaml('cfg_new.yaml')
        self._old_config_partial = self.load_yaml('cfg_old_partial.yaml')
        self._new_config_partial = self.load_yaml('cfg_new_partial.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def load_json(self, filename):
        return json.loads(self.get_fixture_content(filename))

    @property
    def blank_config(self):
        return self._blank_config

    @property
    def old_config(self):
        return self._old_config

    @property
    def new_config(self):
        return self._new_config

    @property
    def new_config_partial(self):
        return self._new_config_partial

    @property
    def old_config_partial(self):
        return self._old_config_partial

    def test_run_config_blank(self):
        self.assertRaises(ValueError, self.action_cls, self.blank_config)

    def test_run_config_old(self):
        self.assertRaises(ValueError, self.action_cls, self.old_config)

    def test_run_config_new(self):
        action = self.get_action_instance(self.new_config)
        self.assertIsInstance(action, self.action_cls)
        return action

    def test_run_config_old_partial(self):
        self.assertRaises(ValueError, self.action_cls, self.old_config_partial)

    def test_run_config_new_partial(self):
        action = self.get_action_instance(self.new_config_partial)
        self.assertRaises(KeyError, action.establish_connection,
                          vsphere="default")

    def mock_one_vm(self, vm_id):
        """
        Configure a single VM mock.  Helps make writing tests against vm actions easier.

        Args:
        - vm_id: the MOID to give the mock VM

        Returns:
        - (action, mock_vm)
        """
        action = self.test_run_config_new()
        action.establish_connection = mock.Mock()
        action.si_content = mock.Mock()
        action.si_content.rootFolder = mock.Mock()
        action.si_content.viewManager = mock.Mock()
        mock_vm = mock.Mock()
        mock_vm._moId = vm_id
        container = mock.Mock()
        container.view = mock.MagicMock()
        container.view.__iter__.return_value = [mock_vm]
        action.si_content.viewManager.CreateContainerView.return_value =\
            container
        return (action, mock_vm)
