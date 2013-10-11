# -*- coding: UTF-8 -*-

import os
import ConfigParser
import execnet

from sqlalchemy.exc import OperationalError

from xivo_dao.helpers import config as dao_config
from xivo_dao.helpers import db_manager
from xivo_lettuce.ssh import SSHClient
from xivo_lettuce.ws_utils import RestConfiguration, WsUtils
import xivo_ws


_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


class XivoAcceptanceConfig(object):

    def __init__(self):
        self._config = self._read_config()

        self.asterisk_conn = None
        self.xivo_conn = None

        self.xivo_host = self._config.get('xivo', 'hostname')
        self.xivo_biz_host = self._config.get('xivo_biz', 'hostname')

        self.ssh_login = self._config.get('ssh_infos', 'login')

        self.browser_enable = self._config.getboolean('browser', 'enable')
        self.browser_visible = self._config.getboolean('browser', 'visible')
        self.browser_timeout = self._config.getint('browser', 'timeout')
        self.browser_resolution = self._config.get('browser', 'resolution')

        self.webi_url = 'https://%s' % self.xivo_host
        self.webi_login = self._config.get('login_infos', 'login')
        self.webi_password = self._config.get('login_infos', 'password')

        self.callgen_host = self._config.get('callgen', 'hostname')
        self.callgen_login = self._config.get('callgen', 'login')

        self.rest_username = self._config.get('webservices_infos', 'login')
        self.rest_passwd = self._config.get('webservices_infos', 'password')
        self.rest_protocol = self._config.get('restapi', 'protocol')
        self.rest_port = self._config.getint('restapi', 'port')

        self.xc_login_timeout = self._config.getint('xivo_client', 'login_timeout')

        self.kvm_hostname = self._config.get('kvm_infos', 'hostname')
        self.kvm_login = self._config.get('kvm_infos', 'login')
        self.kvm_vm_name = self._config.get('kvm_infos', 'vm_name')
        self.kvm_shutdown_timeout = int(self._config.get('kvm_infos', 'shutdown_timeout'))
        self.kvm_boot_timeout = int(self._config.get('kvm_infos', 'boot_timeout'))

    def setup(self):
        self._setup_dao()
        self._setup_ssh_client()
        self._setup_ws()

    def _read_config(self):
        config = ConfigParser.RawConfigParser()
        config_environ = os.getenv('LETTUCE_CONFIG')
        if config_environ and os.path.exists(config_environ):
            config_file = config_environ
        else:
            local_config = '%s.local' % _CONFIG_FILE
            if os.path.exists(local_config):
                config_file = local_config
            else:
                config_file = _CONFIG_FILE
        with open(config_file) as fobj:
            config.readfp(fobj)
        return config

    def _setup_dao(self):
        dao_config.DB_URI = 'postgresql://asterisk:proformatique@%s/asterisk' % self.xivo_host
        dao_config.XIVO_DB_URI = 'postgresql://xivo:proformatique@%s/xivo' % self.xivo_host
        db_manager.reinit()
        try:
            self.asterisk_conn = db_manager._asterisk_engine
            self.xivo_conn = db_manager._xivo_engine
        except OperationalError:
            print 'PGSQL ERROR: could not connect to server'

    def _setup_ssh_client(self):
        self.ssh_client_xivo = SSHClient(self.xivo_host, self.ssh_login)
        self.ssh_client_callgen = SSHClient(self.callgen_host, self.callgen_login)

    def _setup_ws(self):
        self.restapi_config_1_0 = RestConfiguration(self.rest_protocol,
                                                    self.xivo_host,
                                                    self.rest_port,
                                                    self.rest_username,
                                                    self.rest_passwd,
                                                    '1.0')
        self.restapi_config_1_1 = RestConfiguration(self.rest_protocol,
                                                    self.xivo_host,
                                                    self.rest_port,
                                                    self.rest_username,
                                                    self.rest_passwd,
                                                    '1.1')
        self.ws_utils = xivo_ws.XivoServer(self.xivo_host,
                                           self.rest_username,
                                           self.rest_passwd)
        self.restapi_utils_1_0 = WsUtils(self.restapi_config_1_0)
        self.restapi_utils_1_1 = WsUtils(self.restapi_config_1_1)

    @property
    def execnet_gateway(self):
        try:
            return self._execnet_gateway
        except AttributeError:
            self._execnet_gateway = execnet.makegateway('ssh=%s@%s' % (self.ssh_login, self.xivo_host))
            return self._execnet_gateway
