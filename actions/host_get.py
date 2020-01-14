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

from vmwarelib import inventory
from vmwarelib.serialize import HostGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class GetHost(BaseAction):

    def run(self, host_ids, host_names, vsphere=None):
        """
        Retrieve summary information for given Hosts (ESXi)

        Args:
        - host_ids: Moid of Host to retrieve
        - host_names: Name of Host to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)


        Returns:
        - dict: Host network hints details.
        """
        self.establish_connection(vsphere)

        results = None
        if not host_ids and not host_names:
            results = self.get_all_hosts()
        else:
            results = self.get_select_hosts(host_ids, host_names)

        return results

    def get_select_hosts(self, host_ids, host_names):
        results = {}
        if host_ids:
            for hid in host_ids:
                host = inventory.get_hostsystem(self.si_content, moid=hid)
                if host:
                    if host.name not in results:
                        results[host.name] = json.loads(json.dumps(host.summary,
                                                                   cls=HostGetJSONEncoder))
        if host_names:
            for host in host_names:
                host = inventory.get_hostsystem(self.si_content, name=host)
                if host:
                    if host.name not in results:
                        results[host.name] = json.loads(json.dumps(host.summary,
                                                                   cls=HostGetJSONEncoder))

        return results

    def get_all_hosts(self):
        results = {}
        container = inventory.get_managed_entities(self.si_content, vim.HostSystem)
        for host in container.view:
            results[host.name] = json.loads(json.dumps(host.summary,
                                                       cls=HostGetJSONEncoder))

        return results
