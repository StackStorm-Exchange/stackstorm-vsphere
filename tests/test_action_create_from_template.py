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

import eventlet
import mock
import threading
import vm_create_from_template

from datetime import datetime
from vsphere_base_action_test_case import VsphereBaseActionTestCase
from pyVmomi import vim  # pylint: disable-msg=E0611

__all__ = [
    'CreateFromTemplateTestCase'
]


class CreateFromTemplateTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = vm_create_from_template.VMCreateFromTemplate

    def setUp(self):
        super(CreateFromTemplateTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    @mock.patch.object(vm_create_from_template, 'vim')
    @mock.patch.object(vm_create_from_template, 'inventory')
    def test_action_with_queued_state(self, mock_inventory, mock_vim):
        # To check task state, set to return TaskInfo.State value
        mock_vim.TaskInfo.State = vim.TaskInfo.State

        mock_task = mock.Mock()
        mock_task.info.state = vim.TaskInfo.State.queued
        mock_template = mock.Mock()
        mock_template.CloneVM_Task.return_value = mock_task
        mock_inventory.get_virtualmachine.return_value = mock_template

        params = {
            'name': 'creating_vm',
            'template_id': 'vm-1',
            'datacenter_id': 'datacenter-1',
            'resourcepool_id': 'resourcepool-1',
            'datastore_id': 'datastore-1',
        }

        # creating and starting mock task
        mock_task_thread = MockTaskThread(mock_task)
        mock_task_thread.start()

        result = self._action.run(**params)

        self.assertTrue(result[0])

        # stopping mock task
        mock_task_thread.stop()

    @mock.patch.object(vm_create_from_template, 'vim')
    @mock.patch.object(vm_create_from_template, 'inventory')
    def test_action_with_queued_state_and_failed(self, mock_inventory, mock_vim):
        # To check task state, set to return TaskInfo.State value
        mock_vim.TaskInfo.State = vim.TaskInfo.State

        mock_task = mock.Mock()
        mock_task.info.state = vim.TaskInfo.State.queued
        mock_template = mock.Mock()
        mock_template.CloneVM_Task.return_value = mock_task
        mock_inventory.get_virtualmachine.return_value = mock_template

        params = {
            'name': 'creating_vm',
            'template_id': 'vm-1',
            'datacenter_id': 'datacenter-1',
            'resourcepool_id': 'resourcepool-1',
            'datastore_id': 'datastore-1',
        }

        # creating and starting mock task which will fail finally
        mock_task_thread = MockTaskThread(mock_task, will_fail=True)
        mock_task_thread.start()

        result = self._action.run(**params)

        self.assertFalse(result[0])

        # stopping mock task
        mock_task_thread.stop()


# This is the class to emulate the Task to change the state every second.
class MockTaskThread(threading.Thread):
    def __init__(self, mock_task, will_fail=False):
        super(MockTaskThread, self).__init__()

        self.mock_task = mock_task
        self.is_stopped = False
        self.woken_time = datetime.now()
        self.final_state = vim.TaskInfo.State.success
        if will_fail:
            self.final_state = vim.TaskInfo.State.error

    def run(self):
        while not self.is_stopped:
            passed_seconds = (datetime.now() - self.woken_time).seconds
            if passed_seconds > 2:
                self.mock_task.info.state = self.final_state
            elif passed_seconds > 1:
                self.mock_task.info.state = vim.TaskInfo.State.running

            eventlet.sleep()

    def stop(self):
        self.is_stopped = True
        self.join(1)
