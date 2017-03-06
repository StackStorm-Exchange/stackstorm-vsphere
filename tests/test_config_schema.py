import mock
import yaml
import json
import re

from st2client import shell
from st2client.utils import httpclient
from st2client.models.core import ConfigManager

from st2tests.http import FakeResponse
from st2tests.pack_resource import BasePackResourceTestCase


class ConfigSchemaTestCase(BasePackResourceTestCase):
    def setUp(self):
        super(ConfigSchemaTestCase, self).setUp()

        self.shell = shell.Shell()
        self._content_schema = yaml.load(self.get_fixture_content('config.schema.yaml'))
        self._new_config = yaml.load(self.get_fixture_content('cfg_new.yaml'))

    @mock.patch.object(httpclient.HTTPClient, 'get')
    @mock.patch.object(ConfigManager, 'update')
    @mock.patch('st2client.commands.pack.editor')
    @mock.patch('st2client.utils.interactive.prompt')
    def test_set_schema(self, mock_prompt, mock_editor, mock_config_update, mock_http_get):
        # set dummy HTTP response from the st2api
        dummy_api_response = {
            'id': 'dummy1234',
            'pack': 'vsphere',
            'attributes': self._content_schema
        }
        mock_http_get.return_value = FakeResponse(json.dumps(dummy_api_response), 200, 'OK')

        # set dummy paramters
        def side_effect_prompt(msg, **kwargs):
            if re.compile(r'^ssl_verify').match(msg):
                return 'y'
            elif re.compile(r'^default.host').match(msg):
                return '192.168.0.1'
            elif re.compile(r'^default.port').match(msg):
                return '443'
            elif re.compile(r'^default.user').match(msg):
                return 'Admin'
            elif re.compile(r'^default.passwd').match(msg):
                return 'password'
            elif re.compile(r'^taskinfo.tasknum').match(msg):
                return '5'
            else:
                return None
        mock_prompt.side_effect = side_effect_prompt

        # skip modification by editor
        def side_effect_editor(contents):
            return contents
        mock_editor.edit.side_effect = side_effect_editor

        # check for the result configuration is expected
        def side_effect_config_update(config):
            self.assertEqual(config.pack, 'vsphere')

            # check for generated configuration has expected parameters
            for k, v in self._new_config.items():
                self.assertEqual(config.values[k], v)

            return config
        mock_config_update.side_effect = side_effect_config_update

        # execute pack config command
        ret = self.shell.run(['--debug', 'pack', 'config', 'vsphere'])

        self.assertEqual(ret, 0)
