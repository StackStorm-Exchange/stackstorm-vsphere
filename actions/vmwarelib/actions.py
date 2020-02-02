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

import ssl
import atexit

import eventlet
import requests
from pyVim import connect  # pylint: disable=no-name-in-module
from pyVmomi import vim  # pylint: disable-msg=E0611

from st2common.runners.base_action import Action

from vmwarelib.tagging import VmwareTagActions

CONNECTION_ITEMS = ['host', 'port', 'user', 'passwd']


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "vsphere" in config:
            if config['vsphere'] is None:
                raise ValueError("'vsphere' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

        ssl_verify = config.get('ssl_verify', None)
        if ssl_verify is False:
            # Don't print out ssl warnings
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

    def establish_connection(self, vsphere):
        """
        Sets:
        - content
        """
        self.si = self._connect(vsphere)
        self.si_content = self.si.RetrieveContent()

    @property
    def content(self):
        return self.si_content

    def _get_connection_info(self, vsphere):
        if vsphere:
            connection = self.config['vsphere'].get(vsphere)
        else:
            connection = self.config['vsphere'].get('default')

        for item in CONNECTION_ITEMS:
            if item in connection:
                pass
            else:
                raise KeyError("vsphere.yaml Mising: vsphere:%s:%s"
                               % (vsphere, item))

        return connection

    def _connect(self, vsphere):
        connection = self._get_connection_info(vsphere)

        try:
            si = connect.SmartConnect(host=connection['host'],
                                      port=connection['port'],
                                      user=connection['user'],
                                      pwd=connection['passwd'])
        except Exception as e:
            raise Exception(e)

        atexit.register(connect.Disconnect, si)
        return si

    def connect_rest(self, vsphere):
        connection = self._get_connection_info(vsphere)

        session = requests.Session()
        session.verify = self.config['ssl_verify']
        session.auth = (connection['user'], connection['passwd'])

        if connection['port'] == 80:
            transport = "http"
        elif connection['port'] == 443:
            transport = "https"
        else:
            raise ValueError("Port %s is invalid" % connection['port'])

        url_base = "%s://%s" % (transport, connection['host'])
        self.tagging = VmwareTagActions(session=session, url_base=url_base)

        login_url = url_base + "/rest/com/vmware/cis/session"

        session.post(login_url)

        return session

    def _rest_api_call(self, vsphere, api_endpoint, api_verb, payload=None):
        # The connection info is needed to add the hostname to the API endpoint
        connection = self._get_connection_info(vsphere)

        session = self.connect_rest(vsphere)

        api_endpoint = "https://%s%s" % (connection['host'], api_endpoint)

        # Create a prepared request so we can use the verb that was passed
        req = requests.Request(api_verb, api_endpoint, json=payload)
        prepped = session.prepare_request(req)

        response = session.send(prepped)

        return response.json()

    def _wait_for_task(self, task):
        while (task.info.state == vim.TaskInfo.State.queued or   # noqa: W504
               task.info.state == vim.TaskInfo.State.running):
            eventlet.sleep(1)
        return task.info.state == vim.TaskInfo.State.success

    def get_vim_type(self, object_type):
        try:
            return getattr(vim, object_type)
        except AttributeError:
            raise AttributeError("specified object_type ('%s') is not supported" % object_type)
