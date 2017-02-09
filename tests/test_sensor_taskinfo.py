import mock
import yaml

from st2tests.base import BaseSensorTestCase
from taskinfo_sensor import TaskInfoSensor

from pyVim import connect
from datetime import datetime


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

    def test_no_dispatching_taskinfo(self):
        sensor = self.get_sensor_instance(config=self.cfg_new)

        sensor.setup()

        # replace TaskHistoryCollector object by mock that returns empty list
        sensor._collector = mock.Mock()
        sensor._collector.ReadNextTasks = mock.Mock(return_value=[])

        sensor.poll()

        contexts = self.get_dispatched_triggers()

        self.assertEqual(contexts, [])

    class MockTaskInfo(object):
        def __init__(self, taskid='Task-1', op_name='VirtualMachine.clone'):
            self.key = taskid
            self.descriptionId = op_name
            self.queueTime = datetime.now()
            self.startTime = datetime.now()
            self.completeTime = datetime.now()
