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

import socket
from pyVmomi import vim  # pylint: disable-msg=E0611

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMCreateFromTemplate(BaseAction):
    NETWORK_PARAMS = [u'ipaddr', u'netmask', u'gateway', u'domain']

    def run(self, name, template_id, datacenter_id, resourcepool_id,
            datastore_id, vsphere=None, networks=[]):
        is_success = True
        self.establish_connection(vsphere)

        # convert ids to stubs
        template = inventory.get_virtualmachine(self.si_content, template_id)
        datacenter = inventory.get_datacenter(self.si_content, datacenter_id)
        resourcepool = inventory.get_resource_pool(self.si_content,
                                                   resourcepool_id)
        datastore = inventory.get_datastore(self.si_content, datastore_id)
        # prep objects for consumption
        target_folder = datacenter.vmFolder

        # relocate spec
        relocatespec = vim.vm.RelocateSpec()
        relocatespec.datastore = datastore
        relocatespec.pool = resourcepool

        # When the customize parameters for the network-adapters are specified,
        # this makes a configration to customize a deploying virtual machine.
        # (By default, this customizes nothing)
        custom_adapters = []
        for network in networks:
            # The validator for the 'networks' parameter is needed because of
            # the restriction[*1] that there is no validation processing for the
            # array type value in the action parameter yet.
            #
            # [*1] https://github.com/StackStorm/st2/issues/3160
            if not self._validate_networks_param(network):
                break

            # set customize configuration to set IP address to the network adapters.
            adaptermap = vim.vm.customization.AdapterMapping()
            adaptermap.adapter = vim.vm.customization.IPSettings()
            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            adaptermap.adapter.ip.ipAddress = network.get('ipaddr', '0.0.0.0')
            adaptermap.adapter.subnetMask = network.get('netmask', '255.255.255.0')
            adaptermap.adapter.gateway = network.get('gateway', '0.0.0.0')

            custom_adapters.append(adaptermap)

        # clone spec
        clonespec = vim.vm.CloneSpec()
        clonespec.location = relocatespec
        clonespec.powerOn = False
        clonespec.template = False

        # customize networ adapter only when the networks parameter is specified
        if custom_adapters:
            customspec = vim.vm.customization.Specification()

            customspec.identity = vim.vm.customization.LinuxPrep(
                domain=network.get('domain', 'localhost'),
                hostName=vim.vm.customization.FixedName(name=name))
            customspec.nicSettingMap = custom_adapters
            customspec.globalIPSettings = vim.vm.customization.GlobalIPSettings()

            clonespec.customization = customspec

        task = template.CloneVM_Task(folder=target_folder, name=name,
                                     spec=clonespec)
        self._wait_for_task(task)
        if task.info.state != vim.TaskInfo.State.success:
            is_success = False
            self.logger.warning(task.info.error.msg)

        return (is_success, {'task_id': task._moId, 'vm_id': task.info.result._moId})

    def _validate_networks_param(self, param):
        # Checks parameter value type
        if not isinstance(param, dict):
            self.logger.warning("Invalid 'networks' parameter(%s) is specified" % str(param))
            return False

        # Checks unnecessary parameters are specified
        if not all([x in self.NETWORK_PARAMS for x in param.keys()]):
            self.logger.warning("The unnecessary keys are specified")
            return False

        # Checks all IP Address informations are corrected
        try:
            [socket.inet_aton(param[x]) for x in [u'ipaddr', u'netmask', u'gateway'] if x in param]
        except socket.error:
            self.logger.warning("Invalid IP Address is specified in the 'networks'")
            return False

        return True
