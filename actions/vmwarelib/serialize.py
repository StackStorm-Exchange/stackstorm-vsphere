import json

from pyVmomi import vim, vmodl  # pylint: disable-msg=E0611

# List of classes which are not JSON serializable
NON_JSON_SERILIZABLE_TYPES = [
    vim.Network.Summary,
    vim.Datastore.Summary,
    vim.Description,
    vim.ClusterComputeResource.Summary,
    vim.host.Summary,
    vim.host.Summary.HardwareSummary,
    vim.host.Summary.ConfigSummary,
    vim.Network,
    vim.AboutInfo,
    vim.GuestInfo,
    vim.GuestInfo.DiskInfo,
    vim.GuestInfo.NicInfo,
    vim.GuestInfo.ScreenInfo,
    vim.GuestInfo.StackInfo,
    vim.net.DnsConfigInfo,
    vim.net.IpConfigInfo,
    vim.net.IpConfigInfo.IpAddress,
    vim.net.IpRouteConfigInfo,
    vim.net.IpRouteConfigInfo.Gateway,
    vim.net.IpRouteConfigInfo.IpRoute,
    vim.option.OptionValue,
    vim.SharesInfo,
    vim.StorageResourceManager.IOAllocationInfo,
    vim.vm.ConfigInfo,
    vim.vm.Summary,
    vim.vm.Summary.ConfigSummary,
    vim.vm.Summary.StorageSummary,
    vim.vm.Summary.GuestSummary,
    vim.vm.ToolsConfigInfo,
    vim.vm.ToolsConfigInfo.ToolsLastInstallInfo,
    vim.Datastore,
    vim.vm.RuntimeInfo,
    vim.vm.DeviceRuntimeInfo,
    vim.vm.device.ParaVirtualSCSIController,
    vim.vm.device.VirtualDevice.PciBusSlotInfo,
    vim.vm.device.VirtualDisk,
    vim.vm.device.VirtualDisk.FlatVer2BackingInfo,
    vim.vm.device.VirtualLsiLogicController,
    vim.vm.device.VirtualLsiLogicSASController,
    vim.vm.VirtualHardware,
    vmodl.DynamicProperty
]

PHYSICAL_NIC_NON_JSON_SERILIZABLE_TYPES = [
    vim.host.PhysicalNic,
    vim.host.PhysicalNic.NetworkHint,
    vim.host.PhysicalNic.NetworkHint.IpNetwork,
    vim.host.PhysicalNic.NetworkHint.NamedNetwork,
    vim.host.PhysicalNic.LldpInfo,
    vim.host.PhysicalNic.CdpInfo,
    vim.host.PhysicalNic.CdpDeviceCapability,
    vmodl.KeyAnyValue,
]

VM_RUNTIME_INFO_NON_JSON_SERILIZABLE_TYPES = [
    vim.HostSystem,
    vim.vm.RuntimeInfo,
    vim.vm.RuntimeInfo.DasProtectionState,
    vim.vm.DeviceRuntimeInfo,
    vim.vm.DeviceRuntimeInfo.VirtualEthernetCardRuntimeState,
    vim.vm.FeatureRequirement,
    vim.host.FeatureMask,
    vim.host.Summary,
]

HOST_GET_NON_JSON_SERILIZABLE_TYPES = [
    vim.AboutInfo,
    vim.ElementDescription,
    vim.HostSystem,
    vim.host.Summary,
    vim.host.Summary.ConfigSummary,
    vim.host.Summary.QuickStats,
    vim.host.Summary.HardwareSummary,
    vim.host.SystemIdentificationInfo,
]


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        try:
            return super(MyJSONEncoder, self).default(obj)
        except TypeError:
            if type(obj) in NON_JSON_SERILIZABLE_TYPES:
                return obj.__dict__

            # For anything else just return the class name
            return "__{}__".format(obj.__class__.__name__)


class HostGetJSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        try:
            return super(HostGetJSONEncoder, self).default(obj)
        except TypeError:
            if type(obj) in HOST_GET_NON_JSON_SERILIZABLE_TYPES:
                return obj.__dict__

            # For anything else just return the class name
            return "__{}__".format(obj.__class__.__name__)


class PhysicalNicJSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        try:
            return super(PhysicalNicJSONEncoder, self).default(obj)
        except TypeError:
            if type(obj) in PHYSICAL_NIC_NON_JSON_SERILIZABLE_TYPES:
                return obj.__dict__

            # For anything else just return the class name
            return "__{}__".format(obj.__class__.__name__)


class VmRuntimeInfoJSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        try:
            return super(VmRuntimeInfoJSONEncoder, self).default(obj)
        except TypeError:
            if type(obj) in VM_RUNTIME_INFO_NON_JSON_SERILIZABLE_TYPES:
                return obj.__dict__

            # For anything else just return the class name
            return "__{}__".format(obj.__class__.__name__)
