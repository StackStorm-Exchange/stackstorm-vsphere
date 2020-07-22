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
from vmwarelib.serialize import NetworkGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class NetworkGet(BaseAction):
    def get_network_dict(self, network):
        is_dvs = False
        if isinstance(network, vim.dvs.DistributedVirtualPortgroup):
            is_dvs = True

        summary = json.loads(json.dumps(network.summary, cls=NetworkGetJSONEncoder))
        return_dict = {
            'name': network.name,
            'id': summary['network']['_moId'],
            'is_dvs': is_dvs,
            'summary': summary
        }

        return return_dict

    def get_all(self):
        results = []
        networks = inventory.get_managed_entities(self.si_content, vim.Network)
        for network in networks.view:
            results.append(self.get_network_dict(network))

        return results

    def get_by_id_or_name(self, network_ids=[], network_names=[]):
        results = []

        for did in network_ids:
            network = inventory.get_network(self.si_content, moid=did)
            if network and network.name not in results:
                results.append(self.get_network_dict(network))

        for network in network_names:
            network = inventory.get_network(self.si_content, name=network)
            if network and network.name not in results:
                results.append(self.get_network_dict(network))

        return results

    def run(self, network_ids, network_names, vsphere=None):
        """
        Retrieve summary information for given networks (ESXi)

        Args:
        - network_ids: Moid of network to retrieve
        - network_names: Name of network to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: network objects
        """
        return_results = []

        self.establish_connection(vsphere)

        if not network_ids and not network_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(network_ids, network_names)

        return return_results
