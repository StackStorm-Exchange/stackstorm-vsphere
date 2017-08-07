# Change Log

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

