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
from template_get import TemplateGet
from vsphere_base_action_test_case import VsphereBaseActionTestCase

__all__ = [
    'TemplateGet'
]


class TemplateGetTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = TemplateGet

    def setUp(self):
        super(TemplateGetTestCase, self).setUp()

        self._action = self.get_action_instance(self.new_config)

        self._action.establish_connection = mock.Mock()
        self._action.si_content = mock.Mock()

    def test_get_template_dict(self):
        template_1 = mock.Mock()
        template_1_name_property = mock.PropertyMock(return_value='test_template')
        type(template_1).name = template_1_name_property
        expected_sumary = {
            'vm': {
                '_moId': 1
            }
        }
        template_1.summary = expected_sumary
        template_1._moId = 1

        expected_result = {
            'name': 'test_template',
            'id': 1,
            'summary': expected_sumary
        }

        result = self._action.get_template_dict(template_1)
        self.assertEqual(result, expected_result)

    def test_get_by_id_or_name(self):
        template_1 = mock.Mock()
        template_1_name_property = mock.PropertyMock(return_value='test_template')
        type(template_1).name = template_1_name_property
        expected_sumary_1 = {
            'vm': {
                '_moId': 1
            }
        }
        template_1.summary = expected_sumary_1
        template_1._moId = 1

        template_2 = mock.Mock()
        template_2_name_property = mock.PropertyMock(return_value='test_template_2')
        type(template_2).name = template_2_name_property
        expected_sumary_2 = {
            'vm': {
                '_moId': 2
            }
        }
        template_2.summary = expected_sumary_2
        template_2._moId = 2

        template_3 = mock.Mock()
        template_3_name_property = mock.PropertyMock(return_value='test_template_3')
        type(template_3).name = template_3_name_property
        expected_sumary_3 = {
            'vm': {
                '_moId': 3
            }
        }
        template_3.summary = expected_sumary_3
        template_3._moId = 3

        template_4 = mock.Mock()
        template_4_name_property = mock.PropertyMock(return_value='test_template_4')
        type(template_4).name = template_4_name_property
        expected_sumary_4 = {
            'vm': {
                '_moId': 4
            }
        }
        template_4.summary = expected_sumary_4
        template_4._moId = 4

        template_5 = mock.Mock()
        template_5_name_property = mock.PropertyMock(return_value='test_template_5')
        type(template_5).name = template_5_name_property
        expected_sumary_5 = {
            'vm': {
                '_moId': 5
            }
        }
        template_5.summary = expected_sumary_5
        template_5._moId = 5

        mock_view = mock.Mock(view=[template_1,
                                    template_2,
                                    template_3,
                                    template_4,
                                    template_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_template_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_template_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_template_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.get_by_id_or_name([4], ['test_template_2', 'test_template_5'])
        self.assertEqual(result, expected_result)

    def test_get_all_templates(self):
        template_1 = mock.Mock()
        template_1_name_property = mock.PropertyMock(return_value='test_template')
        type(template_1).name = template_1_name_property
        expected_sumary_1 = {
            'vm': {
                '_moId': 1
            }
        }
        template_1.summary = expected_sumary_1
        template_1._moId = 1

        template_2 = mock.Mock()
        template_2_name_property = mock.PropertyMock(return_value='test_template_2')
        type(template_2).name = template_2_name_property
        expected_sumary_2 = {
            'vm': {
                '_moId': 2
            }
        }
        template_2.summary = expected_sumary_2
        template_2._moId = 2

        mock_view = mock.Mock(view=[template_1, template_2])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_template',
                'id': 1,
                'summary': expected_sumary_1
            }, {
                'name': 'test_template_2',
                'id': 2,
                'summary': expected_sumary_2
            }
        ]

        result = self._action.get_all()
        self.assertEqual(result, expected_result)

    def test_run_get_by_id_or_name(self):
        template_1 = mock.Mock()
        template_1_name_property = mock.PropertyMock(return_value='test_template')
        type(template_1).name = template_1_name_property
        expected_sumary_1 = {
            'vm': {
                '_moId': 1
            }
        }
        template_1.summary = expected_sumary_1
        template_1._moId = 1

        template_2 = mock.Mock()
        template_2_name_property = mock.PropertyMock(return_value='test_template_2')
        type(template_2).name = template_2_name_property
        expected_sumary_2 = {
            'vm': {
                '_moId': 2
            }
        }
        template_2.summary = expected_sumary_2
        template_2._moId = 2

        template_3 = mock.Mock()
        template_3_name_property = mock.PropertyMock(return_value='test_template_3')
        type(template_3).name = template_3_name_property
        expected_sumary_3 = {
            'vm': {
                '_moId': 3
            }
        }
        template_3.summary = expected_sumary_3
        template_3._moId = 3

        template_4 = mock.Mock()
        template_4_name_property = mock.PropertyMock(return_value='test_template_4')
        type(template_4).name = template_4_name_property
        expected_sumary_4 = {
            'vm': {
                '_moId': 4
            }
        }
        template_4.summary = expected_sumary_4
        template_4._moId = 4

        template_5 = mock.Mock()
        template_5_name_property = mock.PropertyMock(return_value='test_template_5')
        type(template_5).name = template_5_name_property
        expected_sumary_5 = {
            'vm': {
                '_moId': 5
            }
        }
        template_5.summary = expected_sumary_5
        template_5._moId = 5

        mock_view = mock.Mock(view=[template_1,
                                    template_2,
                                    template_3,
                                    template_4,
                                    template_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_template_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_template_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_template_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run([4], ['test_template_2', 'test_template_5'])
        self.assertEqual(result, expected_result)

    def test_run_all(self):
        template_1 = mock.Mock()
        template_1_name_property = mock.PropertyMock(return_value='test_template')
        type(template_1).name = template_1_name_property
        expected_sumary_1 = {
            'vm': {
                '_moId': 1
            }
        }
        template_1.summary = expected_sumary_1
        template_1._moId = 1

        template_2 = mock.Mock()
        template_2_name_property = mock.PropertyMock(return_value='test_template_2')
        type(template_2).name = template_2_name_property
        expected_sumary_2 = {
            'vm': {
                '_moId': 2
            }
        }
        template_2.summary = expected_sumary_2
        template_2._moId = 2

        template_3 = mock.Mock()
        template_3_name_property = mock.PropertyMock(return_value='test_template_3')
        type(template_3).name = template_3_name_property
        expected_sumary_3 = {
            'vm': {
                '_moId': 3
            }
        }
        template_3.summary = expected_sumary_3
        template_3._moId = 3

        template_4 = mock.Mock()
        template_4_name_property = mock.PropertyMock(return_value='test_template_4')
        type(template_4).name = template_4_name_property
        expected_sumary_4 = {
            'vm': {
                '_moId': 4
            }
        }
        template_4.summary = expected_sumary_4
        template_4._moId = 4

        template_5 = mock.Mock()
        template_5_name_property = mock.PropertyMock(return_value='test_template_5')
        type(template_5).name = template_5_name_property
        expected_sumary_5 = {
            'vm': {
                '_moId': 5
            }
        }
        template_5.summary = expected_sumary_5
        template_5._moId = 5

        mock_view = mock.Mock(view=[template_1,
                                    template_2,
                                    template_3,
                                    template_4,
                                    template_5])
        mock_vmware = mock.Mock(rootFolder="folder")
        mock_vmware.viewManager.CreateContainerView.return_value = mock_view
        self._action.si_content = mock_vmware

        expected_result = [
            {
                'name': 'test_template',
                'id': 1,
                'summary': expected_sumary_1
            }, {
                'name': 'test_template_2',
                'id': 2,
                'summary': expected_sumary_2
            }, {
                'name': 'test_template_3',
                'id': 3,
                'summary': expected_sumary_3
            }, {
                'name': 'test_template_4',
                'id': 4,
                'summary': expected_sumary_4
            }, {
                'name': 'test_template_5',
                'id': 5,
                'summary': expected_sumary_5
            }
        ]

        result = self._action.run(None, None)
        self.assertEqual(result, expected_result)
