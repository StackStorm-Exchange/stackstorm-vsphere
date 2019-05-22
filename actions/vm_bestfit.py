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
from vmwarelib.actions import BaseAction
import re


class BestFit(BaseAction):

    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(BestFit, self).__init__(config)

    def get_host(self, cluster_name):
        """Return a host from the given cluster that's powered on and has the least number of VMs
        :param cluster_name: Name of the cluster to retrieve a host from
        :returns host_obj: Host object from the given cluster
        """
        vimtype = self.get_vim_type("HostSystem")

        hosts = inventory.get_managed_entities(self.si_content, vimtype)

        host_obj = None
        least_vms = None

        for host in hosts.view:
            # Need to verify that the host is on, connected, and not in maintenance mode
            # powerState can be 'poweredOff' 'poweredOn' 'standBy' 'unknown'
            if (host.parent.name == cluster_name and
                    host.runtime.powerState == 'poweredOn' and
                    host.runtime.inMaintenanceMode is False):
                # Find the host that has the least number of VMs on it
                if (least_vms is None or len(host.vm) < least_vms):
                    host_obj = host
                    least_vms = len(host.vm)

        if host_obj is not None:
            return host_obj
        else:
            raise Exception("No available hosts found for cluster: {}".format(cluster_name))

    def get_storage(self, host, datastore_filter, disks):
        """Return a datastore on the host that is either specified in the disks variable or
        has the most free space and a name that doesn't match any filters
        :param host: Host object to retrieve a datastore from
        :param datastore_filter: Object containing list of filtersto exclude certain datastores
          :example: ["string1", "string2"]
        :param disks: Object containing a list of disks to add to the VM
          :example:
            [{
               "size_gb": "string",
               "uuid": "string",
               "datastore": "string",
               "controller_bus": "string",
               "scsi_bus": "string"
            }]
        :returns datastore: Datastore object from the given host
        """
        datastore = None

        # First check the disks variable for a datastotre to use
        if disks is not None:
            first_disk = disks[0]
            datastore_name = first_disk['datastore']
            # If the disks variable is given and it's datastore key is not "automatic" then
            # the datastore from the disks variable will be returned
            if datastore_name != "automatic":
                vimtype = self.get_vim_type("Datastore")
                datastore = inventory.get_managed_entity(self.si_content, vimtype,
                                                         name=datastore_name)

        # If the disks variable is empty or the datastore is set to "automatic" then search
        # the available datastores on the host for the one with the most free space
        if datastore is None:
            storages = host.datastore
            most_space = 0
            for ds in storages:
                # The following function returns False if the name of the datastore
                # matches any of the regex filters
                if self.filter_datastores(ds.name, datastore_filter):
                    if ds.info.freeSpace > most_space:
                        datastore = ds
                        most_space = ds.info.freeSpace

        return datastore

    def filter_datastores(self, datastore_name, datastore_filter_regex_list):
        """Check if a datastore should be filtered from the list or not.
        If no regex filters are given then all datastores can be used
        :param datastore_name: Name of the datastore to check filters for
        :param datastore_filter: Array containing list of filters to exclude certain datastores
        :returns boolean: True if the datastore name does NOT match any of the regex expressions
        """
        if datastore_filter_regex_list is None:
            return True

        # Filter out the datastores by name
        # Include if the datastore name does NOT match any of the regex expressions
        for regex in datastore_filter_regex_list:
            if re.search(regex.strip(), datastore_name):
                return False
        return True

    def run(self, cluster_name, datastore_filter_regex_list, disks, vsphere=None):
        """
        Returns a host and datastore name and MOID from the given cluster and filters.
        The result host will be the one with the least amount of VMs and the result
        datastore will be the one with the most free space

        Args:
        - cluster_name: Name of the cluster in vSphere to get a host from
        - datastore_filter_regex_list: List of regular expressions to filter the list of datastores
        - disks: List of disks to attach to a new VM
        - vsphere: Pre-Configured vsphere connection details

        Returns:
        - dict: key value pairs with calculated host and datastore names and ids
        """
        self.establish_connection(vsphere)

        # Return a host from the given cluster that's powered on and has the least amount of VMs
        host = self.get_host(cluster_name)

        # Return a datastore on the host that is either specified in the disks variable or
        # has the most free space and a name that doesn't match any filters
        datastore = self.get_storage(host, datastore_filter_regex_list, disks)

        return {'clusterName': host.parent.name,
                'hostName': host.name,
                'hostID': host._moId,
                'datastoreName': datastore.name,
                'datastoreID': datastore._moId}
