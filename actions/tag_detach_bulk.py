# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vmwarelib.actions import BaseAction


class TagDetachBulk(BaseAction):
    def run(self, bulk_object_type,
            category_name, category_cardinality,
            query_object_type, query_object_name,
            tag_name,
            vsphere):
        self.connect_rest(vsphere)

        # create the category and tags
        category = self.tagging.category_find_by_name(category_name)
        if not category:
            return "Category doesn't exist: category={}".format(category_name)

        tag = self.tagging.tag_find_by_name(tag_name, category['id'])
        if not tag:
            return "Tag doesn't exist: category={} tag={}".format(category_name, tag_name)

        return self.tagging.tag_bulk(query_object_type=query_object_type,
                                     query_object_name=query_object_name,
                                     bulk_object_type=bulk_object_type,
                                     category=category_name,
                                     tag=tag_name,
                                     cardinality=category_cardinality,
                                     action='detach')
