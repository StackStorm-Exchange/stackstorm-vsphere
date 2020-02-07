import ssl
import atexit
import requests

from pyVim import connect  # noqa pylint: disable=no-name-in-module
from st2reactor.sensor.base import PollingSensor


class VSphereSensor(PollingSensor):
    CONNECTION_ITEMS = ['host', 'port', 'user', 'passwd']

    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(VSphereSensor, self).__init__(sensor_service=sensor_service, config=config,
                                            poll_interval=poll_interval)

        if config is None:
            raise ValueError("No connection configuration details found")
        if "vsphere" in config:
            if config['vsphere'] is None:
                raise ValueError("'vsphere' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

        ssl_verify = config.get('ssl_verify', None)
        if ssl_verify is False:
            # Don't print out ssl warnings
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

    def establish_connection(self, vsphere):
        self.si = self._connect(vsphere)
        self.si_content = self.si.RetrieveContent()

    def _connect(self, vsphere):
        connection = self.config['vsphere'].get(vsphere)
        for item in self.CONNECTION_ITEMS:
            if item in connection:
                pass
            else:
                raise KeyError("vsphere.yaml Mising: vsphere:%s:%s"
                               % (vsphere, item))

        try:
            si = connect.SmartConnect(host=connection['host'],
                                      port=connection['port'],
                                      user=connection['user'],
                                      pwd=connection['passwd'])
        except Exception as e:
            raise Exception(e)

        atexit.register(connect.Disconnect, si)
        return si

    def _get_config_entry(self, key, prefix=None):
        # First of all, get configuration value from Datastore
        value = self.sensor_service.get_value('vsphere.%s' % (key), local=False)
        if value:
            return value

        # Then, get it from the configuration file
        config = self.config
        if prefix:
            for _prefix in prefix.split('.'):
                config = config.get(_prefix, {})

        return config.get(key, None)
