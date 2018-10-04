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

from pyVmomi import vim, vmodl  # pylint: disable-msg=E0611
from vmwarelib.actions import BaseAction

import copy
import datetime
import json
import pyVmomi


class GetProperties(BaseAction):

    def run(self, type, property, id, raw, vsphere=None):
        """
        Leverage the Property Collector to retrieve properties from any
        Managed Object.

        Args:
        - type: vimType
        - properties: optional array of properties to get (default: all)
        - ids: optional array of MOIDs to limit results (default: all)
        - vsphere: pre-configured connection information

        Returns:
        - dict: key = moid, value = dict of properties
        """

        self.establish_connection(vsphere)
        return self.collect(self.si_content, type, property, id, raw)

    def collect(self, content, type, properties, ids, raw):
        """
        Leverage the Property Collector to retrieve properties from any
        Managed Object.

        Args:
        - content: service instance content
        - type: object type
        - properties: optional array of properties to get (default: all)
        - ids: optional array of MOIDs to limit results (default: all)

        Returns:
        - dict: key = moid, value = dict of properties
        """

        vimtype = getattr(vim, type)

        rootFolder = content.rootFolder
        viewMgr = content.viewManager
        if not ids:
            view = viewMgr.CreateContainerView(container=rootFolder,
                                               type=[vimtype],
                                               recursive=True)
        else:
            view = viewMgr.CreateListView()
            for id in ids:
                view.ModifyListView(add=[
                    pyVmomi.VmomiSupport.GetWsdlType('urn:vim25', type)(id)])

        traversal_spec = vmodl.query.PropertyCollector.TraversalSpec()
        traversal_spec.name = 'traverseEntities'
        traversal_spec.path = 'view'
        traversal_spec.skip = False
        traversal_spec.type = view.__class__

        obj_spec = vmodl.query.PropertyCollector.ObjectSpec()
        obj_spec.obj = view
        obj_spec.skip = True
        obj_spec.selectSet = [traversal_spec]

        property_spec = vmodl.query.PropertyCollector.PropertySpec()
        property_spec.type = vimtype
        if not properties:
            property_spec.all = True
        else:
            property_spec.pathSet = properties

        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = [obj_spec]
        filter_spec.propSet = [property_spec]

        rawdata = content.propertyCollector.RetrieveContents([filter_spec])
        return self.transform(ids, rawdata) if not raw else rawdata

    def jsonify_vsphere_obj(self, obj):
        """JSONify a vSphere Managed/Data object."""
        class PyVmomiObjectJSONEncoder(json.JSONEncoder):
            """Custom JSON encoder to encode vSphere object."""
            def __init__(self, *args, **kwargs):
                super(PyVmomiObjectJSONEncoder, self).__init__(*args, **kwargs)

            def default(self, obj):  # pylint: disable=method-hidden
                if isinstance(obj, datetime.datetime):
                    return pyVmomi.Iso8601.ISO8601Format(obj)
                elif isinstance(obj, pyVmomi.VmomiSupport.DataObject):
                    # eliminate the very annoying Dynamic fields if empty
                    if (obj.__dict__['dynamicType'] is None and
                            len(obj.__dict__['dynamicProperty']) == 0):
                        tmp = copy.deepcopy(obj.__dict__)
                        tmp.pop('dynamicType')
                        tmp.pop('dynamicProperty')
                        return tmp
                    return obj.__dict__
                elif isinstance(obj, pyVmomi.VmomiSupport.ManagedObject):
                    return unquote(obj).split(':')[-1]
                elif isinstance(obj, type):
                    return str(obj)
                return json.JSONEncoder.default(self, obj)
        return json.loads(PyVmomiObjectJSONEncoder().encode(obj))

    def transform(self, ids, rawdata):
        result = {}
        for obj in rawdata:
            objid = unquote(obj.obj).split(':')[-1]
            ps = {}
            for prop in obj.propSet:
                ps[unquote(prop.name)] = self.jsonify_vsphere_obj(prop.val)
            result[objid] = ps
        return (not ids or sorted(result.keys()) == sorted(ids), result)


def unquote(item):
    return str(item).strip("'")
