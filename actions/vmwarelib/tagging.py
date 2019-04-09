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


class VmwareTagActions(object):
    # vSphere Automation API (6.5)
    # API Reference: https://code.vmware.com/web/dp/explorer-apis?id=191
    def __init__(self, session, url_base):
        self.session = session
        self.url_base = url_base

    ############################################################################

    # Request Actions

    def make_url(self, endpoint):
        return self.url_base + endpoint

    def get(self, endpoint):
        url = self.make_url(endpoint)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, payload=None):
        url = self.make_url(endpoint)
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        if response.text:
            return response.json()
        return None

    def delete(self, endpoint, payload=None):
        url = self.make_url(endpoint)
        response = self.session.delete(url, json=payload)
        response.raise_for_status()
        if response.text:
            return response.json()
        return None

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
                "associable_types": ["VirtualMachine"]}  # One or more VMWARE_OBJECT_TYPES

    def category_create(self, name, description=None, cardinality=None,
                        associable_types=None):
        create_spec = self.category_create_spec()
        create_spec['name'] = name
        if description:
            create_spec['description'] = description
        if cardinality:
            create_spec['cardinality'] = cardinality
        if associable_types is not None:
            create_spec['associable_types'] = associable_types

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
            response = self.post("/rest/com/vmware/cis/tagging/tag/id:{}?~action="
                                 "list-tags-for-category".format(category_id))
        else:
            response = self.get("/rest/com/vmware/cis/tagging/tag")
        return response["value"]

    def tag_get(self, tag_id):
        response = self.get("/rest/com/vmware/cis/tagging/tag/id:{}".format(tag_id))
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

    ############################################################################

    # Tag Association Functions

    def tag_association_endpoint(self, action, tag_id=None):
        if tag_id:
            return "/rest/com/vmware/cis/tagging/tag-association/id:{}?~action={}".format(tag_id,
                                                                                          action)
        else:
            return "/rest/com/vmware/cis/tagging/tag-association?~action={}".format(action)

    def tag_association_attach(self, tag_id, obj_type, obj_id):
        return self.post(self.tag_association_endpoint("attach", tag_id),
                         payload={"object_id": {"id": obj_id,
                                                "type": obj_type}})

    def tag_association_attach_multiple(self, tag_ids, obj_type, obj_id):
        return self.post(self.tag_association_endpoint("attach-multiple-tags-to-object"),
                         payload={"tag_ids": tag_ids,
                                  "object_id": {"id": obj_id,
                                                "type": obj_type}})

    def tag_association_detach(self, tag_id, obj_type, obj_id):
        return self.post(self.tag_association_endpoint("detach", tag_id),
                         payload={"object_id": {"id": obj_id,
                                                "type": obj_type}})

    def tag_association_list_attached_tags(self, obj_type, obj_id):
        response = self.post(self.tag_association_endpoint("list-attached-tags"),
                             payload={"object_id": {"id": obj_id,
                                                    "type": obj_type}})
        return response['value']

    def tag_association_list_attached_objects(self, tag_id):
        response = self.post(self.tag_association_endpoint("list-attached-objects",
                                                           tag_id))
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
