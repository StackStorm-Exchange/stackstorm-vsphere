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

import copy
import datetime
import mock
import pyVmomi

from get_properties import GetProperties
from pyVmomi import vim  # pylint: disable-msg=E0611
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'GetPropertiesTestCase'
]


class GetPropertiesTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetProperties

    transformed = {
        "vm-22": {
            "config.hardware.memoryMB": 10240,
            "dataobj-dyn": {
                "arguments": "arguments",
                'dynamicType': "Hello",
                'dynamicProperty': [],
                "envVariables": ["A=B", "C=D"],
                "programPath": "cmd.exe",
                "workingDirectory": "/tmp"
            },
            "guest.ipAddress": "10.99.0.4",
            "name": "VCSA",
            "network": ["network-15"],
            "time": "1992-01-12T01:01:22Z"
        },
        "vm-46": {
            "config.hardware.memoryMB": 2048,
            "dataobj-nodyn": {
                "arguments": "arguments",
                "envVariables": ["A=B", "C=D"],
                "programPath": "cmd.exe",
                "workingDirectory": "/tmp"
            },
            "guest.ipAddress": "fe80::250:56ff:feb4:cfb9",
            "name": "testvm",
            "network": [],
            "time": "1992-01-17T01:01:46Z"
        }
    }

    def setUp(self):
        def mockDynamicProperty(name, val):
            result = mock.Mock()
            result.name = name
            result.val = val
            return result
        super(GetPropertiesTestCase, self).setUp()
        self._action = self.get_action_instance(self.new_config)
        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()
        self._action.si_content.rootFolder = mock.Mock()
        self._action.si_content.viewManager = mock.Mock()
        self._action.si_content.viewManager.CreateContainerView = mock.Mock()
        self._action.si_content.viewManager.CreateListView = mock.Mock()
        self._action.si_content.propertyCollector = mock.Mock()
        cmdspec22 = vim.vm.guest.ProcessManager.ProgramSpec(
            arguments="arguments",
            envVariables=["A=B", "C=D"],
            programPath="cmd.exe",
            workingDirectory='/tmp')
        cmdspec46 = copy.deepcopy(cmdspec22)
        cmdspec22.__dict__['dynamicType'] = 'Hello'
        # mock up the raw objects used to test transform
        vm22 = mock.Mock()
        vm22.obj = 'vim.VirtualMachine:vm-22'
        vm22.propSet = [mockDynamicProperty("config.hardware.memoryMB", 10240),
                        mockDynamicProperty("dataobj-dyn", cmdspec22),
                        mockDynamicProperty("guest.ipAddress", "10.99.0.4"),
                        mockDynamicProperty("name", "VCSA"),
                        mockDynamicProperty("network", [
                                            pyVmomi.VmomiSupport.GetWsdlType(
                                                'urn:vim25', 'Network')(
                                                    'network-15')]),
                        mockDynamicProperty("time",
                                            datetime.datetime(
                                                1992, 1, 12, 1, 1, 22))]
        vm46 = mock.Mock()
        vm46.obj = 'vim.VirtualMachine:vm-46'
        vm46.propSet = [mockDynamicProperty("config.hardware.memoryMB", 2048),
                        mockDynamicProperty("dataobj-nodyn", cmdspec46),
                        mockDynamicProperty("guest.ipAddress",
                                            "fe80::250:56ff:feb4:cfb9"),
                        mockDynamicProperty("name", "testvm"),
                        mockDynamicProperty("network", []),
                        mockDynamicProperty("time",
                                            datetime.datetime(
                                                1992, 1, 17, 1, 1, 46))]
        self.raw = [vm22, vm46]

    @mock.patch('pyVmomi.vmodl.query.PropertyCollector')
    def test_simple_property_by_id(self, pc):
        with mock.patch.object(
            self._action.si_content.propertyCollector, 'RetrieveContents',
                return_value=self.raw):
            result = self._action.run(type='VirtualMachine',
                                      id=['vm-22', 'vm-46'],
                                      property=['does.not.exist'], raw=False)
            assert self._action.si_content.viewManager.CreateListView.called
            # status True because every object was found
            self.assertEqual(result, (True, self.transformed))
        with mock.patch.object(
            self._action.si_content.propertyCollector, 'RetrieveContents',
                return_value=self.raw):
            result = self._action.run(type='VirtualMachine',
                                      id=['vm-22', 'vm-46', 'vm-47'],
                                      property=None, raw=False)
            # status False because not every object was found
            self.assertEqual(result, (False, self.transformed))

    @mock.patch('pyVmomi.vmodl.query.PropertyCollector')
    def test_simple_by_type(self, pc):
        with mock.patch.object(
            self._action.si_content.propertyCollector, 'RetrieveContents',
                return_value=self.raw):
            result = self._action.run(type='VirtualMachine', id=None,
                                      property=None, raw=False)
            assert\
                self._action.si_content.viewManager.CreateContainerView.called
            self.assertEqual(result, (True, self.transformed))

    @mock.patch('pyVmomi.vmodl.query.PropertyCollector')
    def test_raw_output(self, pc):
        with mock.patch.object(
            self._action.si_content.propertyCollector, 'RetrieveContents',
                return_value=self.raw):
            result = self._action.run(type='VirtualMachine', id=None,
                                      property=None, raw=True)
            self.assertNotEqual(result, self.transformed)
