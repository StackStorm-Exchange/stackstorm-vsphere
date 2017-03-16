import mock
import yaml
import time

from st2tests.base import BaseSensorTestCase
from taskinfo_sensor import TaskInfoSensor

from pyVim import connect
from pyVmomi import vim
from datetime import datetime, timedelta


class TaskInfoSensorTestCase(BaseSensorTestCase):
    sensor_cls = TaskInfoSensor

    def setUp(self):
        super(TaskInfoSensorTestCase, self).setUp()

        self.cfg_new = yaml.safe_load(self.get_fixture_content('cfg_new.yaml'))

        # replace the processing to connect vSphere by mock
        connect.SmartConnect = mock.Mock()

    def test_dispatching_taskinfo(self):
        sensor = self.get_sensor_instance(config=self.cfg_new)

        sensor.setup()

        # replace TaskHistoryCollector object by mock that returns dummy TaskInfo object
        sensor._collector = mock.Mock()
        sensor._collector.ReadNextTasks = mock.Mock(return_value=[self.MockTaskInfo('task-0')])

        sensor.poll()

        contexts = self.get_dispatched_triggers()

        self.assertNotEqual(contexts, [])
        self.assertEqual(len(contexts), 1)
        self.assertEqual(contexts[0]['payload']['task_id'], 'task-0')
        self.assertNotEqual(contexts[0]['payload']['queue_time'], '')
        self.assertNotEqual(contexts[0]['payload']['start_time'], '')
        self.assertNotEqual(contexts[0]['payload']['complete_time'], '')
        self.assertEqual(contexts[0]['payload']['state'], 'success')

    def test_no_dispatching_taskinfo(self):
        sensor = self.get_sensor_instance(config=self.cfg_new)

        sensor.setup()

        # replace TaskHistoryCollector object by mock that returns empty list
        sensor._collector = mock.Mock()
        sensor._collector.ReadNextTasks = mock.Mock(return_value=[])

        sensor.poll()

        contexts = self.get_dispatched_triggers()

        self.assertEqual(contexts, [])

    def test_dispatching_uncompleted_taskinfo(self):
        sensor = self.get_sensor_instance(config=self.cfg_new)

        sensor.setup()

        # replace TaskHistoryCollector object by mock that returns dummy TaskInfo object
        sensor._collector = mock.Mock()
        sensor._collector.ReadNextTasks = mock.Mock(
                return_value=[self.MockUncompletedTaskInfo('task-1')])

        sensor.poll()

        # wait until dummy processing completes
        time.sleep(2)

        contexts = self.get_dispatched_triggers()

        self.assertNotEqual(contexts, [])
        self.assertEqual(len(contexts), 2)

        self.assertEqual(contexts[0]['payload']['task_id'], 'task-1')
        self.assertEqual(contexts[0]['payload']['state'], 'running')
        self.assertNotEqual(contexts[0]['payload']['queue_time'], '')
        self.assertNotEqual(contexts[0]['payload']['start_time'], '')
        self.assertEqual(contexts[0]['payload']['complete_time'], '')

        self.assertEqual(contexts[1]['payload']['task_id'], 'task-1')
        self.assertEqual(contexts[1]['payload']['state'], 'success')
        self.assertNotEqual(contexts[1]['payload']['complete_time'], '')

    class MockTaskInfo(object):
        def __init__(self, taskid='Task-1', op_name='VirtualMachine.clone'):
            self.key = taskid
            self.descriptionId = op_name
            self.queueTime = datetime.now()
            self.startTime = datetime.now()
            self.completeTime = datetime.now()
            self.state = str(vim.TaskInfo.State.success)
            self.task = mock.Mock()
            self.task.info = self

    class MockUncompletedTaskInfo(object):
        def __init__(self, taskid='Task-1', op_name='VirtualMachine.clone'):
            self.key = taskid
            self.descriptionId = op_name
            self.queueTime = datetime.now()
            self.startTime = datetime.now()
            self._completeTime = datetime.now() + timedelta(seconds=1)
            self.task = mock.Mock()
            self.task.info = self

        @property
        def completeTime(self):
            if datetime.now() < self._completeTime:
                return None
            else:
                return self._completeTime

        @property
        def state(self):
            if datetime.now() < self._completeTime:
                return str(vim.TaskInfo.State.running)
            else:
                return str(vim.TaskInfo.State.success)
