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
from vmwarelib.serialize import ClusterGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class ClusterGet(BaseAction):
    def get_cluster_dict(self, cluster):
        summary = json.loads(json.dumps(cluster.summary, cls=ClusterGetJSONEncoder))
        return_dict = {
            'name': cluster.name,
            # extract moid from vim.ManagedEntity object
            'id': str(cluster).split(':')[-1].replace("'", ""),
            'summary': summary
        }

        return return_dict

    def get_all(self):
        clusters = inventory.get_managed_entities(self.si_content, vim.ClusterComputeResource)
        return [self.get_cluster_dict(c) for c in clusters.view]

    def get_by_id_or_name(self, cluster_ids=[], cluster_names=[]):
        results = {}

        for cid in cluster_ids:
            cluster = inventory.get_cluster(self.si_content, moid=cid)
            if cluster and cluster.name not in results:
                results[cluster.name] = self.get_cluster_dict(cluster)

        for cluster in cluster_names:
            cluster = inventory.get_cluster(self.si_content, name=cluster)
            if cluster and cluster.name not in results:
                results[cluster.name] = self.get_cluster_dict(cluster)

        return list(results.values())

    def run(self, cluster_ids, cluster_names, vsphere=None):
        """
        Retrieve summary information for given clusters (ESXi)

        Args:
        - cluster_ids: Moid of cluster to retrieve
        - cluster_names: Name of cluster to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: Datastore objects
        """
        return_results = []

        self.establish_connection(vsphere)

        if not cluster_ids and not cluster_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(cluster_ids, cluster_names)

        return return_results
