# VSphere Integration Pack

This pack integrates with vsphere and allows for the creation and management of Virtual Machines.

## Connection Configuration

You will need to specify the details of the vcenter instance you will be connecting to within 
the `/opt/stackstorm/config/vsphere.yaml` file.

Copy the example configuration in [vsphere.yaml.example](./vsphere.yaml.example)
to `/opt/stackstorm/configs/vsphere.yaml` and edit as required.

You can specify multiple environments using nested values:

```yaml
---
ssl_verify: 
vsphere:
  dev:
    host:
    port:
    user:
    passwd:
  staging:
    host:
    port:
    user:
    passwd:
```
**Note**: Legacy configuration files (`/opt/stackstorm/packs/vsphere/config.yaml`) are no longer supported.
If you are still using this configuration style, you will need to migrate.

If you only have a single vSphere environment, set it up as `default`, and you won't need to specify it when running actions, e.g.:

```yaml
---
ssl_verify: true
vsphere:
  default:
    host: "myvsphere.local"
    port: "443"
    user: "st2"
    passwd: "ItsASecret"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Sensors

### TaskInfoSensor

This sensor observes [TaskInfo](https://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/vim.TaskInfo.html)
which is invoked on the vSphere environment specified in the configuration.

The configuration looks like this:
```yaml
sensors:
  taskinfo:
    tasknum: # indicates the task numbers to check at once
    vsphere:
```
These parameters need to be set:

* `tasknum`: The maximum TaskInfo numbers to get from vCenter at once (By default, `1` is used if this value is omitted).
  If you specify a number > 1, and the number of Tasks that occurred is less than `tasknum`, vCenter returns the actual
  `TaskInfo`s. If more Tasks occurred than `tasknum`, `TaskInfoSensor` dispatches them iteratively until all `TaskInfo`s
  have been received.

* `vsphere`: The name of vSphere environment to observe. This value must be the name of a vSphere
  environment specified in the [Connection Configuration](https://github.com/StackStorm-Exchange/stackstorm-vsphere#connection-configuration).
  If omitted, `default` is used.

### vsphere.taskinfo

This trigger is emitted for every task information that is invoked on the specified vSphere environment in the configuration.

Here is a example of a trigger payload.
```json
{
  state: success,
  queue_time: 2017/03/10 02:08:39,
  start_time: 2017/03/10 02:08:39,
  complete_time: 2017/03/10 02:08:40,
  operation_name: VirtualMachine.destroy,
  task_id: task-5714
}
```
This is what each parameter means:

| params         | description                                                         |
|:---------------|:--------------------------------------------------------------------|
| `state`          | State of the task. The is one of these values: [vim.TaskInfo.State](https://github.com/vmware/pyvmomi/blob/master/docs/vim/TaskInfo/State.rst) |
| `queue_time`     | Time stamp when the task was created                                |
| `start_time`     | Time stamp when the task started running                            |
| `complete_time`  | Time stamp when the task was completed (whether success or failure) |
| `operation_name` | The name of the operation that created the task                     |
| `task_id`        | The MOID (Managed Object Reference ID) that identifies target task  |

## Todo

* Create actions for vsphere environment data retrieval. Allow for integration with external systems for accurate action calls with informed parameter values.
* Expand base test files. Level of mocking required has limited this at present.

## Requirements

This pack requires the python module PYVMOMI. At present the `requirements.txt` specifies version 5.5.0. 
The version specification is to ensure compatibility with Python 2.7.6 (standard version with Ubuntu 14.04).
PYVMOMI 6.0 requires alternative connection coding and Python 2.7.9 minimum due to elements of the SSL module being used.

## Actions

* `vsphere.get_moid` - Returns the MOID of vSphere managed entity corresponding to the specified parameters
* `vsphere.get_vmconsole_urls` - Retrieves urls of the virtual machines' consoles
* `vsphere.get_vms` - Retrieves the virtual machines on a vCenter Server system. It computes the union of Virtual Machine sets based on each parameter.
* `vsphere.hello_vsphere` - Wait for a Task to complete and returns its result.
* `vsphere.set_vm` - Changes configuration of a Virtual Machine.
* `vsphere.vm_check_tools` - Wait for a Task to complete and returns its result.
* `vsphere.vm_create_from_template` - Create a new VM from existing template.
* `vsphere.vm_env_items_get` - Retrieve list of Objects from VSphere
* `vsphere.vm_hw_barebones_create` - Create BareBones VM (CPU, Ram, Graphics Only)
* `vsphere.vm_hw_basic_build` - Minstral Flow to Build Basic Server and power it on.
* `vsphere.vm_hw_cpu_mem_edit` - Adjust the CPU and RAM values assigned to a Virtual Machine
* `vsphere.vm_hw_detail_get` - Retrieve Vsphere Data about a virtual machine
* `vsphere.vm_hw_hdd_add` - Add a HardDrive Object to a Virtual Machine
* `vsphere.vm_hw_moid_get` - Retrieve VM MOID
* `vsphere.vm_hw_nic_add` - Add a Network Device to VM and attach to designated network.
* `vsphere.vm_hw_nic_edit` - Edit Network Device on Virtual machine (V0.2 only allows to switch network)
* `vsphere.vm_hw_power_off` - Perform VM Power off - Equivilant of Holding power button
* `vsphere.vm_hw_power_on` - Power on Virtual Machine
* `vsphere.vm_hw_remove` - Removes the Virtual Machine.
* `vsphere.vm_hw_scsi_controller_add` - Add SCSI HDD Controller device to VM
* `vsphere.vm_hw_uuid_get` - Retrieve VM UUID
* `vsphere.wait_task` - Wait for a Task to complete and returns its result.

## Known Bugs
* Bug: `vm_hw_hdd_add`, Specifying datastore does not work. New files will be added to the same datastore as the core VM files. Note: Specifying a Datastore Cluster does still install files to the correct set of datastores.
