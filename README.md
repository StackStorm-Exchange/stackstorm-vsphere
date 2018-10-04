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
    port: 443
    user: "st2"
    passwd: "ItsASecret"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## What is my VM ID?

Many of the actions in this pack use a VM ID parameter (i.e. in `vmid` or `vm_id` parameters) to determine which VM(s)
to act upon. This is known as a Managed Object Reference ID (MOID). Note that this is **not** the same as the VM's name.

If you use the wrong MOID for one of these actions, you might get this error message:

```
Exception: Inventory Error: Unable to Find Object (<class 'pyVmomi.VmomiSupport.vim.VirtualMachine'>): SuperAwesomeVM
```

This means you're not using the correct MOID. In order to perform an action that requires an ID, you'll have to first
retrieve it's MOID. That can be done with the `vsphere.get_moid` action. For instance, if we wanted to find the MOID
of a VM we called "SuperAwesomeVM", we could feed that into the `vsphere.get_moid` action to retrieve the MOID for
that VM.

```yaml
mierdin@stackstorm:~$ st2 run vsphere.get_moid object_names="SuperAwesomeVM" object_type="VirtualMachine"
.
id: 5a25e85502ebd558f14a686c
status: succeeded
parameters:
  object_names:
  - SuperAwesomeVM
  object_type: VirtualMachine
result:
  exit_code: 0
  result:
    SuperAwesomeVM: '56'
  stderr: ''
  stdout: ''
```

That MOID value (in this case, `56` - you may see something like `vm-123456`) can now be used in other `vsphere` actions
that require an ID.

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
  "state": "success",
  "queue_time": "2017/03/10 02:08:39",
  "start_time": "2017/03/10 02:08:39",
  "complete_time": "2017/03/10 02:08:40",
  "operation_name": "VirtualMachine.destroy",
  "task_id": "task-5714"
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

## Guest Operations

The Guest Operations API allows for direct file and process manipulation inside a virtual machine.
Consider the use case where you want to run a PowerShell script inside a virtual machine.  Here are the steps you would take:

1. Create a PowerShell script in your own pack (for example "mypack/scripts/Return.ps1" - see below)
2. Execute the vsphere.guest_script_run workflow.
3. Examine the result - if the script returns a non-zero exit code, the workflow will fail.  Orquesta [does not allow for output when a workflow fails](https://github.com/StackStorm/st2/issues/4336), so obtaining the exit code, stdout, and stderr from the process requires peeking at the subtasks.

This currently requires a username and password known to the guest to be given as parameters.  It does not yet support vSphere SSO.

The simplest example of this facility is to write a script that exits with the argument given.  Create a script called "Return.ps1" in a pack directory:
```
param (
    [Parameter(Mandatory=$true)][int]$retval
)
echo "This is stdout, going to exit with $retval"
Write-Error "This is stderr, going to exit with $retval"
exit $retval
```

Now execute this script inside the guest using the following command:

    # st2 run vsphere.guest_script_run vm_id=MOID username=USERNAME password=PASSWORD interpreter="C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\PowerShell.EXE" interpreter_arguments="-NonInteractive" script="pack:mypack/scripts/Return.ps1" script_arguments=0

This in turn executes a Orquesta workflow that automates all the steps required:
```
status: succeeded
start_timestamp: Tue, 02 Oct 2018 15:10:08 UTC
end_timestamp: Tue, 02 Oct 2018 15:10:26 UTC
result:
  output:
    exit_code: 0
    stderr: "C:\Users\Administrator\AppData\Local\Temp\stackstorm_vmware246_scriptrunner\Return.ps1 : This is
stderr, going to exit with 0
At line:1 char:1
+ C:\Users\ADMINI~1\AppData\Local\Temp\stackstorm_vmware246_scriptrunne ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
    + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException,Return.ps1

"
    stdout: "This is stdout, going to exit with 0
"
+--------------------------+------------------------+---------------+-----------------------------+-------------------------------+
| id                       | status                 | task          | action                      | start_timestamp               |
+--------------------------+------------------------+---------------+-----------------------------+-------------------------------+
| 5bb38a5156d2c100359a856d | succeeded (2s elapsed) | dir_create    | vsphere.guest_dir_create    | Tue, 02 Oct 2018 15:10:09 UTC |
| 5bb38a5356d2c100359a8570 | succeeded (2s elapsed) | file_upload   | vsphere.guest_file_upload   | Tue, 02 Oct 2018 15:10:11 UTC |
| 5bb38a5656d2c100359a8573 | succeeded (1s elapsed) | process_start | vsphere.guest_process_start | Tue, 02 Oct 2018 15:10:14 UTC |
| 5bb38a5856d2c100359a8576 | succeeded (1s elapsed) | process_wait  | vsphere.guest_process_wait  | Tue, 02 Oct 2018 15:10:16 UTC |
| 5bb38a5a56d2c100359a8579 | succeeded (2s elapsed) | get_stdout    | vsphere.guest_file_read     | Tue, 02 Oct 2018 15:10:18 UTC |
| 5bb38a5d56d2c100359a857c | succeeded (1s elapsed) | get_stderr    | vsphere.guest_file_read     | Tue, 02 Oct 2018 15:10:21 UTC |
| 5bb38a5f56d2c100359a857f | succeeded (2s elapsed) | dir_delete__3 | vsphere.guest_dir_delete    | Tue, 02 Oct 2018 15:10:23 UTC |
+--------------------------+------------------------+---------------+-----------------------------+-------------------------------+
```

Changing the script_arguments to another number results in the action failing.

## Todo

* Create actions for vsphere environment data retrieval. Allow for integration with external systems for accurate action calls with informed parameter values.
* Expand base test files. Level of mocking required has limited this at present.

## Requirements

This pack requires the python module PYVMOMI. At present the `requirements.txt` specifies version 5.5.0. 
The version specification is to ensure compatibility with Python 2.7.6 (standard version with Ubuntu 14.04).
PYVMOMI 6.0 requires alternative connection coding and Python 2.7.9 minimum due to elements of the SSL module being used.

## Actions

* `vsphere.get_moid` - Returns the MOID of vSphere managed entity corresponding to the specified parameters
* `vsphere.get_properties` - Retrieves some or all properties of some or all objects through the PropertyCollector.
* `vsphere.get_vmconsole_urls` - Retrieves urls of the virtual machines' consoles
* `vsphere.get_vms` - Retrieves the virtual machines on a vCenter Server system. It computes the union of Virtual Machine sets based on each parameter.
* `vsphere.guest_dir_create` - Create a directory inside the guest.
* `vsphere.guest_dir_delete` - Delete a directory inside the guest.
* `vsphere.guest_file_create` - Create a file inside the guest.
* `vsphere.guest_file_delete` - Delete a file inside the guest.
* `vsphere.guest_file_read` - Read the contents of a file inside the guest.
* `vsphere.guest_file_upload` - Upload the contents of a file to the guest.
* `vsphere.guest_process_start` - Start a process inside the guest.
* `vsphere.guest_process_wait` - Wait for a process to finish inside the guest.
* `vsphere.guest_script_run` - Orquesta workflow to upload and run a script inside the guest, and capture results.
* `vsphere.hello_vsphere` - Wait for a Task to complete and returns its result.
* `vsphere.host_get` - Retrieves the Summary information for an ESX host.
* `vsphere.host_network_hints_get` - Retrieves the Network Hints for an ESX host.
* `vsphere.set_vm` - Changes configuration of a Virtual Machine.
* `vsphere.vm_check_tools` - Wait for a Task to complete and returns its result.
* `vsphere.vm_create_from_template` - Create a new VM from existing template.
* `vsphere.vm_env_items_get` - Retrieve list of Objects from VSphere (alternatively, use get_properties type=<type> property=name)
* `vsphere.vm_guest_info_get` - Retrieve Guest details of a VM object (deprecated: use get_properties type=VirtualMachine property=guest)
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
* `vsphere.vm_runtime_info_get` - Retrieves the Runtime information for a VM (deprecated: use get_properties type=VirtualMachine property=runtime)
* `vsphere.wait_task` - Wait for a Task to complete and returns its result.

## Known Bugs
* Bug: `vm_hw_hdd_add`, Specifying datastore does not work. New files will be added to the same datastore as the core VM files. Note: Specifying a Datastore Cluster does still install files to the correct set of datastores.
