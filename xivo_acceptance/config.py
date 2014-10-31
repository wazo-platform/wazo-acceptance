# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from configobj import ConfigObj
from execnet.multi import makegateway
import logging
import os

from provd.rest.client.client import new_provisioning_client
from xivo_acceptance.lettuce.ssh import SSHClient
from xivo_acceptance.lettuce.ws_utils import RestConfiguration, WsUtils
from xivo_dao.helpers import config as dao_config
import xivo_ws


logger = logging.getLogger(__name__)

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CONFIG_DIR = (
    os.path.join(os.path.expanduser("~"), '.xivo-acceptance'),
    os.path.join(_ROOT_DIR, 'config')
)
_ASSETS_DIR = (
    '/usr/share/xivo-acceptance/assets',
    os.path.join(_ROOT_DIR, 'data', 'assets')
)
_FEATURES_DIR = (
    '/usr/share/xivo-acceptance/features',
    os.path.join(_ROOT_DIR, 'data', 'features')
)


def load_config(old_config=True):
    XIVO_HOST = os.environ.get('XIVO_HOST', 'daily-xivo-pxe.lan-quebec.avencall.com')

    default_config = {
        'xivo_host': XIVO_HOST,
        'log_file': '/tmp/xivo-acceptance.log',
        'db_uri': 'postgresql://asterisk:proformatique@{}/asterisk'.format(XIVO_HOST),
        'assets_dir': _find_first_existing_path(*_ASSETS_DIR),
        'features_dir': _find_first_existing_path(*_FEATURES_DIR),
        'frontend': {
            'url': 'https://{}'.format(XIVO_HOST),
            'username': 'root',
            'passwd': 'superpass'
        },
        'rest_api': {
            'protocol': 'https',
            'port': 9486,
            'username': 'admin',
            'passwd': 'proformatique'
        },
        'provd': {
            'rest_port': 8667,
            'rest_protocol': 'http',
        },
        'browser': {
            'enable': True,
            'visible': False,
            'timeout': 5,
            'resolution': '1024x768'
        },
        'xivo_client': {
            'login_timeout': 5
        },
        'ssh_login': 'root',
        'jenkins': {
            'hostname': 'jenkins.lan-quebec.avencall.com',
        },
        'linphone': {
            'sip_port_range': '5001,5009',
            'rtp_port_range': '5100,5120'
        },
        'debug': {
            'acceptance': False,
            'selenium': False,
            'linphone': False
        },
        'kvm_infos': {
            'hostname': 'kvm-2-dev.lan-quebec.avencall.com',
            'login': 'root',
            'vm_name': 'openldap-dev',
            'boot_timeout': 30,
            'shutdown_timeout': 5
        },
        'prerequisites': {
            'subnets': [
                '10.0.0.0/8',
                '192.168.0.0/16'
            ]
        }
    }

    if old_config:
        try:
            default_config.update(load_old_config())
        except Exception as e:
            print e

    logger.debug('xivo_host: %s', default_config['xivo_host'])

    return default_config


def load_old_config():
    config = {}
    try:
        default_config_file_path = _find_first_existing_path(*_CONFIG_DIR, suffix='default')
    except Exception as e:
        print e
    else:
        default_config_path = os.path.dirname(default_config_file_path)
        print 'Using default configuration dir {}'.format(default_config_path)

        config_dird = os.path.join(default_config_path, 'conf.d')

        config = ConfigObj(default_config_file_path)

        config_file_extra_absolute = os.getenv('LETTUCE_CONFIG', 'invalid_file_name')
        config_file_extra_in_dird = os.path.join(config_dird, os.getenv('LETTUCE_CONFIG', 'invalid_file_name'))
        config_file_extra_default = os.path.join(config_dird, 'default')
        config_file_extra_local = '%s.local' % config_file_extra_default
        config_file_extra = _find_first_existing_path(config_file_extra_absolute,
                                                      config_file_extra_in_dird,
                                                      config_file_extra_local,
                                                      config_file_extra_default)

        print 'Using extra configuration file {}'.format(config_file_extra)

        config.update(ConfigObj(config_file_extra))

    return config


def _find_first_existing_path(*args, **kwargs):
    for path in args:
        if 'suffix' in kwargs:
            path = os.path.join(path, kwargs['suffix'])
        if path and os.path.exists(path):
            return path
    raise Exception('Directories does not exist: %s' % ' '.join(args))


class XivoAcceptanceConfig(object):

    def __init__(self, config):
        self._config = config
        logger.info("_setup_dao...")
        self._setup_dao()
        logger.info("_setup_ssh_client...")
        self._setup_ssh_client()
        logger.info("_setup_rest_api...")
        self._setup_rest_api()
        logger.info("_setup_provd...")
        self._setup_provd()
        logger.info("_setup_webi...")
        self._setup_webi()

    def _setup_dao(self):
        dao_config.DB_URI = self._config['db_uri']

    def _setup_ssh_client(self):
        self.ssh_client_xivo = SSHClient(hostname=self._config['xivo_host'],
                                         login=self._config['ssh_login'])

    def _setup_rest_api(self):
        rest_config_dict = {
            'protocol': self._config['rest_api']['protocol'],
            'hostname': self._config['xivo_host'],
            'port': self._config['rest_api']['port'],
            'auth_username': self._config['rest_api']['username'],
            'auth_passwd': self._config['rest_api']['passwd']
        }

        rest_config_dict.update({'api_version': '1.1'})
        self.confd_config_1_1 = RestConfiguration(**rest_config_dict)

        self.ws_utils = xivo_ws.XivoServer(host=rest_config_dict['hostname'],
                                           username=rest_config_dict['auth_username'],
                                           password=rest_config_dict['auth_passwd'])
        self.confd_utils_1_1 = WsUtils(self.confd_config_1_1)

    def _setup_provd(self):
        provd_config_obj = RestConfiguration(protocol=self._config['provd']['rest_protocol'],
                                             hostname=self._config['xivo_host'],
                                             port=self._config['provd']['rest_port'],
                                             content_type='application/vnd.proformatique.provd+json')
        self.rest_provd = WsUtils(provd_config_obj)

        provd_url = "http://{host}:{port}/provd".format(host=self._config['xivo_host'],
                                                        port=self._config['provd']['rest_port'])
        self.provd_client = new_provisioning_client(provd_url)

    def _setup_webi(self):
        try:
            command = ['test', '-e', '/var/lib/xivo/configured']
            self.ssh_client_xivo.check_call(command)
        except Exception:
            self.xivo_configured = False
        else:
            self.xivo_configured = True

    @property
    def execnet_gateway(self):
        try:
            return self._execnet_gateway
        except AttributeError:
            spec = 'ssh={login}@{host}'.format(login=self._config['ssh_login'],
                                               host=self._config['xivo_host'])
            self._execnet_gateway = makegateway(spec)
            return self._execnet_gateway
