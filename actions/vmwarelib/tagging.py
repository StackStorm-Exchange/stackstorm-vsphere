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
import argparse
import json
import requests

try:
    import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

# https://vdc-repo.vmware.com/vmwb-repository/dcr-public/1cd28284-3b72-4885-9e31-d1c6d9e26686/71ef7304-a6c9-43b3-a3cd-868b2c236c81/doc/operations/com/vmware/cis/tagging/category.create-operation.html
VMWARE_CARDINALITY = [
    "SINGLE",
    "MULTIPLE",
]

# vSphere Web Services API
# https://code.vmware.com/doc/preview?id=4206#/doc/vmodl.ManagedObjectReference.html
VMWARE_OBJECT_TYPES = [
    'ClusterComputeResource',
    'Datacenter',
    'Datastore',
    'DistributedVirtualPortgroup',
    'DistributedVirtualSwitch',
    'Folder',
    'HostNetwork',
    'HostSystem',
    # 'Library',     # Content Library, REST API is a PITA
    # 'LibraryItem', # Content Library item, REST API is a PITA
    # 'Network',   # duplicate of HostNetwork
    'OpaqueNetwork',
    'ResourcePool',
    # 'StoragePod',  # Not sure what this is, REST API can't query for it
    'VirtualApp',
    'VirtualMachine',
    # 'VmwareDistributedVirtualSwitch', # duplicate of DistributedVirtualSwitch
]

VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR = ("Sorry, VMware REST API doesn't support "
                                        "querying for this type of object")

VMWARE_QUERY_ERROR = "Unable to create a query based on a {} (not supported by VMware API)"

ACTIONS = [
    'attach',
    'replace',
    'detach',
]


class VmwareTagging(object):
    # vSphere Automation API (6.5)
    # API Reference: https://code.vmware.com/web/dp/explorer-apis?id=191
    def __init__(self, server, username, password,
                 scheme="https", port=None, ssl_verify=True, logger=None):
        self.session = requests.Session()
        self.session.verify = ssl_verify
        self.session.auth = (username, password)
        self.server = server
        if port:
            self.url_base = "{}://{}:{}".format(scheme, server, port)
        else:
            self.url_base = "{}://{}".format(scheme, server)

        if logger:
            # use provided logger
            self.logger = logger
        else:
            # create logger from st2common
            try:
                from st2common.runners.utils import get_logger_for_python_runner_action
                self.logger = get_logger_for_python_runner_action(
                    action_name=self.__class__.__name__,
                    log_level='debug')
            except:
                # otherwise create default logger
                import logging
                self.logger = logging.getLogger(__name__)

    ############################################################################

    # Request Actions

    def make_url(self, endpoint):
        return self.url_base + endpoint

    def get(self, endpoint, params=None):
        url = self.make_url(endpoint)
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, payload=None, params=None):
        url = self.make_url(endpoint)
        response = self.session.post(url, params=params, json=payload)
        response.raise_for_status()
        if response.text:
            return response.json()
        return None

    def delete(self, endpoint, payload=None, params=None):
        url = self.make_url(endpoint)
        response = self.session.delete(url, params=params, json=payload)
        response.raise_for_status()
        if response.text:
            return response.json()
        return None

    ############################################################################

    def login(self):
        url = self.make_url("/rest/com/vmware/cis/session")
        response = self.session.post(url, headers={"vmware-use-header-authn": "true"})
        response.raise_for_status()
        # if this succeeds, the cookie is automatically saved in our session
        # however, we'll return the cookie value so that it may be returned
        # to the user
        result = json.loads(response.content)
        self.session.headers.update({"vmware-api-session-id":result["value"]})
        return dict(response.cookies)

    ############################################################################

    # Category Functions

    def category_list(self):
        response = self.get("/rest/com/vmware/cis/tagging/category")
        return response['value']

    def category_get(self, category_id):
        response = self.get("/rest/com/vmware/cis/tagging/category/id:{}".format(category_id))
        return response['value']

    def category_delete(self, category_id):
        response = self.delete("/rest/com/vmware/cis/tagging/category/id:{}".format(category_id))
        return response

    def category_find_by_name(self, name):
        category_id_list = self.category_list()
        for category_id in category_id_list:
            category = self.category_get(category_id)
            if category["name"] == name:
                return category
        return None

    def category_create_spec(self):
        return {"name": "",
                "description": "",
                "cardinality": "SINGLE",  # "SINGLE", "MULTIPLE"
                "associable_types": []}  # One or more VMWARE_OBJECT_TYPES, none/[] = all types

    def category_create(self, name, description=None, cardinality=None,
                        associable_types=None):
        create_spec = self.category_create_spec()
        create_spec['name'] = name
        if description:
            create_spec['description'] = description
        if cardinality:
            if cardinality not in VMWARE_CARDINALITY:
                raise ValueError('Cardinality "{}" does not match the allowed choices: {}'
                                 .format(cardinality, VMWARE_CARDINALITY))
            create_spec['cardinality'] = cardinality

        # default to being able to tag all types
        if associable_types is None or associable_types == []:
            create_spec['associable_types'] = []
        elif isinstance(associable_types, list):
            for at in associable_types:
                if at not in VMWARE_OBJECT_TYPES:
                    raise ValueError('Object type "{}" does not match the allowed choices: {}'
                                     .format(at, VMWARE_OBJECT_TYPES))
            create_spec['associable_types'] = associable_types
        else:
            raise ValueError('Object type must be a list, given: {}'
                             .format(associable_types))

        response = self.post("/rest/com/vmware/cis/tagging/category",
                             payload={'create_spec': create_spec})

        return response['value']

    def category_get_or_create(self, name, description=None, cardinality=None,
                               associable_types=None):
        category = self.category_find_by_name(name)
        if not category:
            # on success this returns the new category's id
            category_id = self.category_create(name, description, cardinality, associable_types)
            category = self.category_get(category_id)
        return category

    ############################################################################

    # Tag Functions

    def tag_list(self, category_id=None):
        # Return all tags from the given category, or all tags from all categories
        if category_id:
            return self.tag_list_for_category(category_id)
        else:
            return self.get("/rest/com/vmware/cis/tagging/tag")['value']

    def tag_get(self, tag_id):
        response = self.get("/rest/com/vmware/cis/tagging/tag/id:{}".format(tag_id))
        return response['value']

    def tag_list_for_category(self, category_id):
        url = ("/rest/com/vmware/cis/tagging/tag/id:{}".format(category_id))
        response = self.post(url, params={'~action': 'list-tags-for-category'})
        return response['value']

    def tag_delete(self, tag_id):
        response = self.delete("/rest/com/vmware/cis/tagging/tag/id:{}".format(tag_id))
        return response

    # If a category ID is not given then this will return the first tag it finds with the given name
    def tag_find_by_name(self, name, category_id=None):
        tag_id_list = self.tag_list(category_id)
        for tag_id in tag_id_list:
            tag = self.tag_get(tag_id)
            if tag['name'] == name:
                return tag
        return None

    def tag_create_spec(self):
        return {"name": "",
                "description": "",
                "category_id": ""}

    def tag_create(self, name, category_id, description=None):
        create_spec = self.tag_create_spec()
        create_spec["name"] = name
        create_spec["category_id"] = category_id
        if description:
            create_spec["description"] = description

        response = self.post("/rest/com/vmware/cis/tagging/tag",
                             payload={"create_spec": create_spec})

        return response["value"]

    # This does not create a new category, it will fail if the given category ID doesn't exist
    def tag_get_or_create(self, name, category_id, description=None):
        tag = self.tag_find_by_name(name, category_id)
        if not tag:
            # on success this returns the new tag's id
            created_tag_id = self.tag_create(name, category_id, description)
            tag = self.tag_get(created_tag_id)
        return tag

    ##############################################################################

    # creates a category and a tag all in one step
    def category_tag_create(self, category, tag, cardinality, associable_types=None):
        category = self.category_get_or_create(category,
                                               cardinality=cardinality,
                                               associable_types=associable_types)
        tag = self.tag_get_or_create(tag, category["id"])
        return (category, tag)

    ############################################################################

    # Tag Association Functions

    def tag_association_endpoint(self, tag_id=None):
        if tag_id:
            return '/rest/com/vmware/cis/tagging/tag-association/id:{}'.format(tag_id)
        else:
            return '/rest/com/vmware/cis/tagging/tag-association'

    def tag_association_attach(self, tag_id, obj_type, obj_id):
        return self.post(self.tag_association_endpoint(tag_id),
                         params={'~action': 'attach'},
                         payload={'object_id': {'id': obj_id,
                                                'type': obj_type}})

    def tag_association_attach_multiple(self, tag_ids, obj_type, obj_id):
        return self.post(self.tag_association_endpoint(),
                         params={'~action': 'attach-multiple-tags-to-object'},
                         payload={'tag_ids': tag_ids,
                                  'object_id': {'id': obj_id,
                                                'type': obj_type}})

    def tag_association_detach(self, tag_id, obj_type, obj_id):
        return self.post(self.tag_association_endpoint(tag_id),
                         params={'~action': 'detach'},
                         payload={'object_id': {'id': obj_id,
                                                'type': obj_type}})

    def tag_association_list_attached_tags(self, obj_type, obj_id):
        response = self.post(self.tag_association_endpoint(),
                             params={'~action': 'list-attached-tags'},
                             payload={'object_id': {'id': obj_id,
                                                    'type': obj_type}})
        return response['value']

    def tag_association_list_attached_objects(self, tag_id):
        response = self.post(self.tag_association_endpoint(tag_id),
                             params={'~action': 'list-attached-objects'})
        return response['value']

    def tag_association_detach_category(self, category_id, obj_type, obj_id):
        # get all tags for this object
        tag_id_list = self.tag_association_list_attached_tags(obj_type, obj_id)

        # if the tag's category matches category_id then detach the tag
        results = []
        for tag_id in tag_id_list:
            tag = self.tag_get(tag_id)
            if tag['category_id'] == category_id:
                self.tag_association_detach(tag_id, obj_type, obj_id)
                results.append(tag)

        return results

    def tag_association_replace(self, tag_id, obj_type, obj_id):
        # remove all tags
        tag = self.tag_get(tag_id)
        self.tag_association_detach_category(tag['category_id'], obj_type, obj_id)

        # attach the provided tag in this category to the object
        return self.tag_association_attach(tag_id, obj_type, obj_id)

    def tag_association_action(self, category, tag, object_type, obj_id, action):
        # action == 'add' or 'replace', one of ACTIONS
        # tag the VM
        self.logger.debug("tag association action... category_id={} tag_id={}"
                          " object_type={} object_id={} action={}"
                          .format(category['id'], tag['id'], object_type, obj_id, action))
        if action == 'attach':
            return self.tag_association_attach(tag['id'], object_type, obj_id)
        elif action == 'replace':
            return self.tag_association_replace(tag['id'], object_type, obj_id)
        elif action == 'detach':
            return self.tag_association_detach_category(category['id'], object_type, obj_id)
        else:
            raise ValueError("Unknown tag association action={} allowed actions are: {}"
                             .format(action, ACTIONS))

    ############################################################################

    def object_find_by_name(self, object_type, name):
        self.logger.debug("Looking for object_type={} name={}".format(object_type, name))
        params = {'filter.names.1': name}
        object_list = self.object_find(object_type, params=params)
        self.object_list_validate_single_element(object_list, object_type, params)
        ids_list = self.object_list_extract_ids(object_list, object_type, params)
        obj_id = ids_list[0]
        self.logger.debug("Found object name={} as object_id={}".format(name, obj_id))
        return obj_id

    def object_list_validate_single_element(self, object_list, object_type, params):
        self.object_list_raise_if_empty(object_list, object_type, params)
        if len(object_list) > 1:
            filter_name, filter_value = self.filter_name_value(params)
            raise ValueError(("Sorry, we found >1 object matching this name in vCenter: "
                              "object_type={} {}={} objects={}").format(object_type,
                                                                        filter_name,
                                                                        filter_value,
                                                                        object_list))

    def object_list_raise_if_empty(self, value, object_type, params):
        if len(value) == 0:
            filter_name, filter_value = self.filter_name_value(params)
            raise ValueError(("Sorry we couldn't find the object you asked for in vCenter: "
                              "object_type={} {}={}").format(object_type,
                                                             filter_name,
                                                             filter_value))

    def object_extract_id(self, obj, object_type, params):
        id_key = self.object_type_id_key(object_type)
        if id_key not in obj:
            filter_name, filter_value = self.filter_name_value(params)
            raise ValueError("Couldn't find the expected ID key in the returned object: "
                             "object_type={} {}={} id_key={} object={}".format(object_type,
                                                                               filter_name,
                                                                               filter_value,
                                                                               id_key,
                                                                               obj))
        return obj[id_key]

    def object_list_extract_ids(self, object_list, object_type, params):
        return [self.object_extract_id(obj, object_type, params) for obj in object_list]

    def object_find(self, object_type, params):
        if object_type not in VMWARE_OBJECT_TYPES:
            raise ValueError('Object type "{}" does not match the allowed choices: {}'
                             .format(object_type, VMWARE_OBJECT_TYPES))

        if object_type == 'ClusterComputeResource':
            return self.cluster_find(params=params)
        elif object_type == 'Datacenter':
            return self.datacenter_find(params=params)
        elif object_type == 'Datastore':
            return self.datastore_find(params=params)
        elif object_type == 'DistributedVirtualPortgroup':
            return self.distributedvirtualportgroup_find(params=params)
        elif object_type == 'DistributedVirtualSwitch':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'Folder':
            return self.folder_find(params=params)
        elif object_type == 'HostNetwork':
            return self.hostnetwork_find(params=params)
        elif object_type == 'HostSystem':
            return self.hostsystem_find(params=params)
        elif object_type == 'Library':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'LibraryItem':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'OpaqueNetwork':
            return self.opaquenetwork_find(params=params)
        elif object_type == 'ResourcePool':
            return self.resourcepool_find(params=params)
        elif object_type == 'StoragePod':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'VirtualApp':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'VirtualMachine':
            return self.vm_find(params=params)

    def filter_name_value(self, params):
        if len(params) == 1 and 'filter.names.1' in params:
            return ('name', params['filter.names.1'])
        else:
            return ('filter', params)

    def object_from_response(self, object_type, params, response, id_key):
        if 'value' not in response:
            raise ValueError("Response from VMware didn't contain the expected"
                             " 'value' key: {}".format(response))

        value = response['value']
        if not isinstance(value, list):
            raise ValueError("response['value'] is not a list, as expected,"
                             " it is a type={} response={}"
                             .format(type(response['value']),
                                     response))
        return value

    def cluster_find(self, params=None):
        response = self.get("/rest/vcenter/cluster", params=params)
        return self.object_from_response('ClusterComputeResoure', params, response, 'cluster')

    def datacenter_find(self, params=None):
        response = self.get("/rest/vcenter/datacenter", params=params)
        return self.object_from_response('Datacenter', params, response, 'datacenter')

    def datastore_find(self, params=None):
        response = self.get("/rest/vcenter/datastore", params=params)
        return self.object_from_response('Datastore', params, response, 'datastore')

    def distributedvirtualportgroup_find(self, params=None):
        params = params if params else {}
        params['filter.types.1'] = 'DISTRIBUTED_PORTGROUP'
        response = self.get("/rest/vcenter/network", params=params)
        return self.object_from_response('DistributedVirtualPortgroup', params, response, 'network')

    def folder_find(self, params=None):
        response = self.get("/rest/vcenter/folder", params=params)
        return self.object_from_response('Folder', params, response, 'folder')

    def hostnetwork_find(self, params=None):
        params = params if params else {}
        params['filter.types.1'] = 'STANDARD_PORTGROUP'
        response = self.get("/rest/vcenter/network", params=params)
        return self.object_from_response('HostNetwork', params, response, 'network')

    def hostsystem_find(self, params=None):
        response = self.get("/rest/vcenter/host", params=params)
        return self.object_from_response('HostSystem', params, response, 'host')

    def opaquenetwork_find(self, params=None):
        params = params if params else {}
        params['filter.types.1'] = 'OPAQUE_NETWORK'
        response = self.get("/rest/vcenter/network", params=params)
        return self.object_from_response('OpaqueNetwork', params, response, 'network')

    def resourcepool_find(self, params=None):
        response = self.get("/rest/vcenter/resource-pool", params=params)
        return self.object_from_response('ResourcePool', params, response, 'resource_pool')

    def vm_find(self, params=None):
        response = self.get("/rest/vcenter/vm", params=params)
        return self.object_from_response('VirtualMachine', params, response, 'vm')

    def object_type_id_key(self, object_type):
        if object_type == 'ClusterComputeResource':
            return 'cluster'
        elif object_type == 'Datacenter':
            return 'datacenter'
        elif object_type == 'Datastore':
            return 'datastore'
        elif object_type == 'DistributedVirtualPortgroup':
            return 'network'
        elif object_type == 'DistributedVirtualSwitch':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'Folder':
            return 'folder'
        elif object_type == 'HostNetwork':
            return 'network'
        elif object_type == 'HostSystem':
            return 'host'
        elif object_type == 'Library':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'LibraryItem':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'OpaqueNetwork':
            return 'network'
        elif object_type == 'ResourcePool':
            return 'resource_pool'
        elif object_type == 'StoragePod':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'VirtualApp':
            raise NotImplementedError(VMWARE_OBJECT_TYPE_UNSUPPORTED_ERROR)
        elif object_type == 'VirtualMachine':
            return 'vm'

    def object_type_filter(self, object_type):
        if object_type == 'ClusterComputeResource':
            return 'filter.clusters'
        elif object_type == 'Datacenter':
            return 'filter.datacenters'
        elif object_type == 'Datastore':
            raise NotImplementedError()
        elif object_type == 'DistributedVirtualPortgroup':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('DistributedVirtualPortgroup'))
        elif object_type == 'DistributedVirtualSwitch':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('DistributedVirtualSwitch'))
        elif object_type == 'Folder':
            return 'filter.folders'
        elif object_type == 'HostNetwork':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('HostNetwork'))
        elif object_type == 'HostSystem':
            return 'filter.hosts'
        elif object_type == 'Library':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('Library'))
        elif object_type == 'LibraryItem':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('LibraryItem'))
        elif object_type == 'OpaqueNetwork':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('OpaqueNetwork'))
        elif object_type == 'ResourcePool':
            return 'filter.hosts'
        elif object_type == 'StoragePod':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('StoragePod'))
        elif object_type == 'VirtualApp':
            raise NotImplementedError(VMWARE_QUERY_ERROR.format('VirtualApp'))
        elif object_type == 'VirtualMachine':
            return 'filter.vms'

    #######################################################################
    def tag_single(self, object_type, object_name,
                   category, tag, cardinality, action):
        obj_id = self.object_find_by_name(object_type, object_name)

        # create the category and tag
        category, tag = self.category_tag_create(category, tag, cardinality)
        # add the tag
        self.tag_association_action(category, tag, object_type, obj_id, action)

    def tag_bulk(self, query_object_type, query_object_name,
                 bulk_object_type,
                 category, tag, cardinality, action):
        obj_id = self.object_find_by_name(query_object_type, query_object_name)

        # create the category and tag
        category, tag = self.category_tag_create(category, tag, cardinality)

        # bulk find all of the objects
        query_obj_type_filter = self.object_type_filter(query_object_type)
        # make parameters look like: {'filter.cluster.1': 'domain-123'}
        params = {query_obj_type_filter + '.1': obj_id}
        object_list = self.object_find(bulk_object_type, params=params)

        # add the tags for all of the objects in the list
        results = []
        for obj in object_list:
            # extract the ID property from the object
            obj_id = self.object_extract_id(obj, bulk_object_type, params)
            response = self.tag_association_action(category, tag,
                                                   bulk_object_type, obj_id, action)
            results.append({
                "id": obj_id,
                "name": obj['name'],
                "type": bulk_object_type,
                "response": response,
            })
        return results


############################################################################

# RawDescriptionHelpFormatter - so that our epilog / examples render newlines properly
# ArgumentDefaultsHelpFormatter - so help strings are show for the arguments
class CliFormatter(argparse.RawDescriptionHelpFormatter,
                   argparse.ArgumentDefaultsHelpFormatter):
    pass


class Cli(object):
    def parse(self):
        parser = argparse.ArgumentParser(
            formatter_class=CliFormatter,
            epilog=self.examples(),
        )

        subparsers = parser.add_subparsers(dest="command")

        ##########################
        # Single
        single_parser = subparsers.add_parser('single',
                                              help="Tags a single object (VM, Cluster, etc)",
                                              formatter_class=CliFormatter,
                                              epilog=self.examples_single())
        single_parser.add_argument('-H', '--hostname', help='VMware vSphere hostname/IP')
        single_parser.add_argument('-U', '--username', help='VMware vSphere username')
        single_parser.add_argument('-P', '--password', help='VMware vSphere password')
        single_parser.add_argument('-c', '--category',
                                   help='Name of the tag category (key) to assign')
        single_parser.add_argument('-t', '--tag',
                                   help='Name of the tag (value) to assign')
        single_parser.add_argument('--cardinality',
                                   help=('How many tags of this category can exist on an'
                                         ' object (one or many)'),
                                   default='SINGLE',
                                   choices=VMWARE_CARDINALITY)
        single_parser.add_argument('--object-name',
                                   help=('Name of the object in vSphere (example: VM name,'
                                         ' cluster name, datastore name, etc)'))
        single_parser.add_argument('--object-type',
                                   help='Type of object to tag',
                                   default='VirtualMachine',
                                   choices=VMWARE_OBJECT_TYPES)
        single_parser.add_argument('-a', '--action',
                                   help='Action to perform on the tag',
                                   default='attach',
                                   choices=ACTIONS)

        ##########################
        # Bulk
        bulk_parser = subparsers.add_parser('bulk',
                                            help="Bulk tags objects based on a query.",
                                            # formatter_class=CliFormatter,
                                            epilog=self.examples_bulk())
        bulk_parser.add_argument('-H', '--hostname', help='VMware vSphere hostname/IP')
        bulk_parser.add_argument('-U', '--username', help='VMware vSphere username')
        bulk_parser.add_argument('-P', '--password', help='VMware vSphere password')
        bulk_parser.add_argument('-c', '--category',
                                 help='Name of the tag category (key) to assign')
        bulk_parser.add_argument('-t', '--tag',
                                 help='Name of the tag (value) to assign')
        bulk_parser.add_argument('--cardinality',
                                 help=('How many tags of this category can exist'
                                       ' on an object (one or many)'),
                                 default='SINGLE',
                                 choices=VMWARE_CARDINALITY)
        bulk_parser.add_argument('-a', '--action',
                                 help='Action to perform on the tag',
                                 default='attach',
                                 choices=ACTIONS)
        bulk_parser.add_argument('--query-object-name',
                                 help=('Name of the object in vSphere to query for'
                                       ' bulk objects. (example: cluster name)'))
        bulk_parser.add_argument('--query-object-type',
                                 help='Type of object to query for sub-objects',
                                 default='ClusterComputeResource',
                                 choices=VMWARE_OBJECT_TYPES)
        bulk_parser.add_argument('--bulk-object-type',
                                 help='Type of object to tag "under" the query object',
                                 default='VirtualMachine',
                                 choices=VMWARE_OBJECT_TYPES)

        return parser.parse_args()

    def examples(self):
        return self.examples_single() + self.examples_bulk()

    def examples_single(self):
        return (
            "examples single:\n"
            "  # Tag a VM with custom_thing = 'hello world'\n"
            "  ./vphere_tagging_cmdb_exclude.py single"
            " -H vsphere.domain.tld"
            " -U username@domain.tld"
            " -P password123"
            " --category 'custom_thing'"
            " --tag 'hello world'"
            " --object-name myvm.domain.tld"
            " --object-type VirtualMachine "
            " --action attach\n"
            "\n"
            "  # Tag a Cluster with custom_thing = 'hello world'\n"
            "  ./vphere_tagging_cmdb_exclude.py single"
            " -H vsphere.domain.tld"
            " -U username@domain.tld"
            " -P password123"
            " --category 'custom_thing'"
            " --tag 'hello world'"
            " --object-name mycluster"
            " --object-type ClusterComputeResource"
            " --action attach\n"
            "\n"
        )

    def examples_bulk(self):
        return (
            "examples bulk:\n"
            "  # Bulk tag all VMs in a Cluster\n"
            "  ./vphere_tagging_cmdb_exclude.py bulk"
            " -H vsphere.domain.tld"
            " -U username@domain.tld"
            " -P password123"
            " --query-object-name 'cls1.dev1'"
            " --query-object-type 'ClusterComputeResource'"
            " --bulk-object-type VirtualMachine"
            " --action attach\n"
            "\n"
        )


if __name__ == "__main__":
    cli = Cli()
    args = cli.parse()

    client = VmwareTagging(args.hostname, args.username, args.password)

    # login
    client.login()

    if args.command == 'single':
        client.tag_single(object_type=args.object_type,
                          object_name=args.name,
                          category=args.category,
                          tag=args.tag,
                          cardinality=args.cardinality,
                          action=args.action)
    elif args.command == 'bulk':
        client.tag_bulk(query_object_type=args.query_object_type,
                        query_object_name=args.query_object_name,
                        bulk_object_type=args.bulk_object_type,
                        category=args.category,
                        tag=args.tag,
                        cardinality=args.cardinality,
                        action=args.action)
    else:
        raise RuntimeError("Unkown command: {}".format(args.command))
