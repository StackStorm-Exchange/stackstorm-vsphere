import json
from pyVmomi import vim  # pylint: disable-msg=E0611


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(MyJSONEncoder, self).default(obj)

        except TypeError:

            if type(obj) in (
                    vim.Network.Summary, vim.Datastore.Summary,
                    vim.ClusterComputeResource.Summary,
                    vim.host.Summary, vim.host.Summary.HardwareSummary,
                    vim.host.Summary.ConfigSummary,
                    vim.Network, vim.AboutInfo, vim.vm.Summary, vim.vm.Summary.ConfigSummary,
                    vim.vm.Summary.StorageSummary, vim.vm.Summary.GuestSummary, vim.Datastore,
                    vim.vm.RuntimeInfo, vim.vm.DeviceRuntimeInfo
            ):
                return obj.__dict__

            # For anything else
            return "__{}__".format(obj.__class__.__name__)
