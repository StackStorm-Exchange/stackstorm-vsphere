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
from vmwarelib.serialize import DatacenterGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class DatacenterGet(BaseAction):
    def get_datacenter_dict(self, datacenter):
        configuration = json.loads(json.dumps(datacenter.configuration,
                                              cls=DatacenterGetJSONEncoder))
        return_dict = {
            'name': datacenter.name,
            # extract moid from vim.ManagedEntity object
            'id': str(datacenter).split(':')[-1].replace("'", ""),
            'configuration': configuration
        }

        return return_dict

    def get_all(self):
        results = []
        datacenters = inventory.get_managed_entities(self.si_content, vim.Datacenter)
        for datacenter in datacenters.view:
            results.append(self.get_datacenter_dict(datacenter))

        return results

    def get_by_id_or_name(self, datacenter_ids=[], datacenter_names=[]):
        results = []

        for did in datacenter_ids:
            datacenter = inventory.get_datacenter(self.si_content, moid=did)
            if datacenter and datacenter.name not in results:
                results.append(self.get_datacenter_dict(datacenter))

        for datacenter in datacenter_names:
            datacenter = inventory.get_datacenter(self.si_content, name=datacenter)
            if datacenter and datacenter.name not in results:
                results.append(self.get_datacenter_dict(datacenter))

        return results

    def run(self, datacenter_ids, datacenter_names, vsphere=None):
        """
        Retrieve summary information for given datacenters (ESXi)

        Args:
        - datacenter_ids: Moid of datacenter to retrieve
        - datacenter_names: Name of datacenter to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: Datacenter objects
        """
        return_results = []

        self.establish_connection(vsphere)

        if not datacenter_ids and not datacenter_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(datacenter_ids, datacenter_names)

        return return_results
