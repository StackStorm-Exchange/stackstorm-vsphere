# Change Log

## v0.16.1

Fixes:
* Fixed bug in `vsphere.tag_*_bulk` where it was erroring if it found no bulk objects
  under the query object (example if a Cluster had no VMs in it).

Contributed by Nick Maludy (@nmaludy Encore Technologies).

## v0.16.0

Additions:
* Added lots of new back-end API functionality to the `vmwarelib.tagging.VmwareTagging` interface.
* Added new `vsphere.tag_attach_bulk` action to attach a tag to a bulk set of resources.
  Primary usecase is tagging all VMs in a cluster dynamically.
* Added new `vsphere.tag_detach_bulk` action to detach a tag from a bulk set of resources.
  Primary usecase is remoave a tag from all VMs in a cluster dynamically.

Contributed by Nick Maludy (@nmaludy Encore Technologies).

## v0.15.1

Changed action:
* `vsphere.tag_attach_or_create` - Added DistributedVirtualPortgroup as a possible object type to be used.
* `vsphere.custom_attr_assign` - Added DistributedVirtualPortgroup as a possible object type to be used.

Contributed by Bradley Bishop (Encore Technologies).

## v0.15.0

Added new action:
* `vsphere.cluster_get` - Retrieve a list of clusters with summary information and an ID from vCenter
* `vsphere.datacenter_get` - Retrieve a list of datacenters with configuration information and an ID from vCenter
* `vsphere.template_get` - Retrieve a list of templates with summary information and an ID from vCenter

Changed action:
* `vsphere.datastore_get` - Fixed action to allow passing ids or names and still work properly. Fixed duplicate check so its working now and the same item is not added twice to the list when specifing name or id.
* `vsphere.network_get` - Fixed action to allow passing ids or names and still work properly. Fixed duplicate check so its working now and the same item is not added twice to the list when specifing name or id.
* `vsphere.get_tags_from_objects` - Fixed action to handle tag categories that can have multiple values. Fixed duplicate check so its working now and the same item is not added twice to the list when specifing name or id.
* `vsphere.vm_hw_basic_build` - Converted from Mistral workflow to Orquesta workflow

Contributed by Bradley Bishop (Encore Technologies).

## v0.14.0

Added new action:
* `vsphere.network_get` - Retrieve a list of networks with summary information and an ID from vCenter

Changed action:
* `vsphere.datastore_get` - Updated the action to include the ID of the datastore in the return.
* `vsphere.affinity_rule_create` - Updated the action to return the name of the hosts that were included in the rule.

Contributed by Bradley Bishop (Encore Technologies).

## v0.13.1
* Force release to get latest tags on repo

## v0.13.0

Added new action:
* `vsphere.get_tags_from_objects` - Retrieves all the tags from an object tags are returned in a dictionary of `category_name: tag_name`

Changed action:
* `vsphere.vm_bestfit` - Added `datastore_filter_strategy` input that is defaulted to `exclude_matches` which is the current behavior. This gives
                         the user more flexibility as to how they want to filter the returned datastores.

Contributed by Bradley Bishop (Encore Technologies).

## v0.12.0

Added new actions:
* `vsphere.datastore_get` - Retrieve a list of datastores with summary information from vCenter
* `vsphere.get_tag_value_from_objects` - Retrieve tag value on a list of object_ids

Contributed by Bradley Bishop (Encore Technologies).

## v0.11.1

Added vim.vm.device.VirtualLsiLogicController object to vmwarelib/serialize.py which was
needed to get the full result from vsphere.vm_hw_scsi_controllers_get

Contributed by John Schoewe (Encore Technologies).

## v0.11.0

Added new actions:
* `vsphere.vm_hw_hdds_get` - Retrieve a list of HDD information from the given VM
* `vsphere.vm_hw_scsi_controllers_get` - Retrieve a list of SCSI controllers on the given VM

Contributed by John Schoewe (Encore Technologies).

## v0.10.0

Added new action:
* `vsphere.vm_snapshots_get` - Returns detailed information about the snapshots.

Contributed by Lionel Seydoux (SPIE ICS).

## v0.9.5

Updated host_get action to get all hosts if not are given. Added tests for action.

Contributed by Bradley Bishop (Encore Technologies).

## v0.9.4

Added action and tests to rename a VM

Contributed by Bradley Bishop (Encore Technologies).

## v0.9.3

Fixed bug in action `vsphere.vm_snapshots_delete`. Where if there were special charaters
in the snapshot name vmware automatically encodes them which was causing the action to fail.

Contributed by Bradley Bishop (Encore Technologies).

## v0.9.2

Fixed bug in action `vsphere.custom_attr_get`. It now ignores datastores that are in
"maintenance mode" if the datastore name is set to "automatic".

Contributed by Nick Maludy (Encore Technologies).

## v0.9.1

Added new action:
* `vsphere.custom_attr_get` - Return the value of the given Custom Attribute on an object

Contributed by John Schoewe (Encore Technologies).

## v0.9.0

Added new action:
* `vsphere.tag_id_get` - Retrieves the ID of a tag with the given category and name

Modified action:
* `vsphere.get_objects_with_tag` - Added ability to get objects with category and tag names

Contributed by John Schoewe (Encore Technologies).

## v0.8.12

Modified action:
* `vsphere.get_vms` - Added VM operating systems to the result

Contributed by John Schoewe (Encore Technologies).

## v0.8.11

* Minor linting fixes triggered by updated flake8 versions in CI

## v0.8.10

Added new action:
* `vsphere.vm_networks_get` - Retrieve a list of network names that the given VM is on

Contributed by John Schoewe (Encore Technologies).

## v0.8.9

Added new action:
* `vsphere.vm_config_info_get` - Retrieve Config Info for given Virtual Machines

Contributed by John Schoewe (Encore Technologies).

## v0.8.8

Added new actions:
* `vsphere.vm_snapshots_delete` - Removes any snapshots older than the specified age. Ignores any snapshots with names that match the given rexex patterns
* `vsphere.vm_bestfit` - Determines the best host and datastore to provision a new VM to on a given cluster

Contributed by John Schoewe (Encore Technologies).

## v0.8.7

Updated actions:
* `vsphere.get_moid` - Returns an error if objects aren't found in vSphere

Contributed by John Schoewe (Encore Technologies).

## v0.8.6

Added new actions:
* `vsphere.get_tag_value_from_object` - Return the value of a tag with a given object ID and category
* `vsphere.vm_resource_pool_get` - Return the MOID of a given VM's containing resource pool

Contributed by John Schoewe (Encore Technologies).

## v0.8.5

Added new tagging.py actions file to vmwarelib.

Added new actions:
* `vsphere.tag_attach_or_create` - Attach a tag to a given object and create the tag and category if they don't exist
* `vsphere.tag_category_create` - Create a vsphere tag category
* `vsphere.tag_category_delete` - Delete a tag category from vSphere
* `vsphere.tag_category_list` - List all tag categories from vSphere
* `vsphere.tag_create` - Create a vSphere tag with the given category
* `vsphere.tag_delete` - Delete a tag from vSphere
* `vsphere.tag_list` - List all tags from a given category or all tags if no category is given
* `vsphere.custom_attr_assign` - Assign a custom attribute in vSphere
* `vsphere.custom_attr_assign_or_create` - Assign a custom attribute in vSphere and create one if it doesn't exist

Added get_vim_type function to vmwarelib/actions.py

Updated actions to use vmwarelib/tagging functions:
* `vsphere.get_objects_with_tag`
* `vsphere.get_tags_on_object`

Renamed action:
* `vsphere.tags_attach_to_object` -> `vsphere.tags_attach_by_id`

Contributed by John Schoewe (Encore Technologies).

## V0.8.4

Added new action:
- `vsphere.vm_tools_options_update` - Update VM tools information

Updated action:
- `vsphere.vm_check_tools` - returns Tools Config as well as tools status

  Contributed by Bradley Bishop (Encore Technologies).

## v0.8.3

Added new actions:
* `vsphere.custom_attr_assign` - Assign a custom attribute to a given object
* `vsphere.tags_attach_to_object` - Attach a list of tags to a given object

Contributed by John Schoewe (Encore Technologies).

## v0.8.2

- guest_process_run was missing the workflow file

## V0.8.1

- Unit tests fixes for python3 updates

  Contributed by Nick Maludy (Encore Technologies).

## V0.8.0

- Disable flake8 on W503 vs W504 line
- Minor linting changes

## v0.7.9

Added new actions:
* `vsphere.affinity_rule_delete` - Deletes an affinity rule
* `vsphere.affinity_rule_create` - Creates an affinity rule and sets the proper informaiton

Contributed by Bradley Bishop (Encore Technologies).

## v0.7.8

* Bumped version to fix tagging issue. No code changes.
* Added a method in vmwarelib/actions.py to connect to the REST API.
* Added new actions:
  * `vsphere.get_objects_with_tag` - return a list of objects with a given vmware tag
  * `vsphere.get_tags_on_object` - return a list of vmware tags on a given object

Contributed by John Schoewe (Encore Technologies).

## V0.7.7

Added a new action actions:
* `vsphere.host_get` - retrieves the Summary information for an ESX host.
* `vsphere.host_network_hints_get` - retrieves the Network Hints for an ESX host.
* `vsphere.vm_guest_info_get` - retrieves the Guest information for a VM.
* `vsphere.vm_runtime_info_get` - retrieves the Runtime information for a VM.

Contributed by Nick Maludy (Encore Technologies).

## V0.7.6

Minor linting fixes

## V0.7.4

Enabled to specify IP Address for each NetworkAdapters in the 'vm_create_from_template' action

## V0.7.3

Fixed the problem to looking over the task state checking in the action library

## V0.7.2

Changed to be able to handle all vim Objects that pyvmomi prepared

## V0.7.1

Fixed non-unique position parameters

## V0.7.0

Updated action `runner_type` from `run-python` to `python-script`

## V0.6.0

Removed `config.yaml`, and updated README to remove references to legacy config support. Pack already supports `config.schema.yaml`

## V0.5.1

Minor linting errors

## V0.5.0

Addition of DataCenter imput field for VM creation action and workflow. Fall back continues to function as present Although this should be provided if Multiple Datacenters are under a single Vsphere instance.

## V0.4.9

Update the `TaskInfoSensor` to enable handling uncompleted Tasks.

## V0.4.8

Update config.schema.yaml to support any name for vcenters

## V0.4.7

Added schema file to apply the configuration schema to this pack.

## V0.4.6

Added 'taskinfo_sensor' to monitor the tasks which is executed on specified vSphere environment.

## V0.4.5

Added 'get_moid' action that enables to get object-id named MOID(Managed Object Reference ID) which is the identifier that uniquely identifies an object in vSphere from object-name and object-type.

## V0.4.4

Added global ssl_verify configuration option to disable SSL certificate verification when connecting to vSphere servers.
Added custom JSON Encoder class to serialize VM summary (`vsphere.vm_hw_details_get`) output, hence, allowing results to be a list of dicts instead of strings. Makes it easier to access the results later in the workflows or action chains.

## V0.4.3

Update nic actions to factor in Distributed Port Groups. When setting a network the DPG will be used over a standard port group of the same name.

## V0.4.2

Updates to actions to factor in ST2 V2 changes forcing string conversions for output and publish variable syntax changes.
vm_basic_build workflow introduction of 12 seconds delay between elements to support parrallel action load balancing

## V0.4.1

Improved error message around Connection/Configuration details. Addition of item get action.

## V0.4

Introduction of Multi Endpoint Configuration.

## V0.3

Clean up of duplicate actions. Addition of moid retrieval function.

## V0.2

Addition of vm_hw atomic actions to create basic Virtual Machine.
