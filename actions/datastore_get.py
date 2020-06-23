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
from vmwarelib.serialize import DatastoreGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class DatastoreGet(BaseAction):
    def get_datastore_dict(self, datastore):
        return_dict = {
            'name': datastore.name,
            'summary': json.loads(json.dumps(datastore.summary, cls=DatastoreGetJSONEncoder))
        }

        return return_dict

    def get_all(self):
        results = []
        datastores = inventory.get_managed_entities(self.si_content, vim.Datastore)
        for datastore in datastores.view:
            results.append(self.get_datastore_dict(datastore))

        return results

    def get_by_id_or_name(self, datastore_ids=[], datastore_names=[]):
        results = []

        for did in datastore_ids:
            datastore = inventory.get_datastore(self.si_content, moid=did)
            if datastore and datastore.name not in results:
                results.append(self.get_datastore_dict(datastore))

        for datastore in datastore_names:
            datastore = inventory.get_datastore(self.si_content, name=datastore)
            if datastore and datastore.name not in results:
                results.append(self.get_datastore_dict(datastore))

        return results

    def run(self, datastore_ids, datastore_names, vsphere=None):
        """
        Retrieve summary information for given datastores (ESXi)

        Args:
        - datastore_ids: Moid of datastore to retrieve
        - datastore_names: Name of datastore to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: Datastore objects
        """
        return_results = []

        self.establish_connection(vsphere)

        if not datastore_ids and not datastore_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(datastore_ids, datastore_names)

        return return_results
