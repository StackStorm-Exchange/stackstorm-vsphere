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
from vmwarelib.serialize import TemplateGetJSONEncoder
from vmwarelib.actions import BaseAction
import json


class TemplateGet(BaseAction):
    def get_template_dict(self, template):
        summary = json.loads(json.dumps(template.summary, cls=TemplateGetJSONEncoder))
        return_dict = {
            'name': template.name,
            'id': summary['vm']['_moId'],
            'summary': summary
        }

        return return_dict

    def get_all(self):
        results = []
        templates = inventory.get_virtualmachines(self.si_content)
        for template in templates.view:
            if template.config.template:
                results.append(self.get_template_dict(template))

        return results

    def get_by_id_or_name(self, template_ids=[], template_names=[]):
        results = []

        for tid in template_ids:
            template = inventory.get_virtualmachine(self.si_content, moid=tid)
            if template and template.config.template and template.name not in results:
                results.append(self.get_template_dict(template))

        for template in template_names:
            template = inventory.get_virtualmachine(self.si_content, name=template)
            if template and template.config.template and template.name not in results:
                results.append(self.get_template_dict(template))

        return results

    def run(self, template_ids, template_names, vsphere=None):
        """
        Retrieve summary information for given templates (ESXi)

        Args:
        - template_ids: Moid of template to retrieve
        - template_names: Name of template to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: Template objects
        """
        return_results = []

        self.establish_connection(vsphere)

        if not template_ids and not template_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(template_ids, template_names)

        return return_results
