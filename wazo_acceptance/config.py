# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

from copy import deepcopy
from xivo.config_helper import parse_config_dir
from xivo.chain_map import ChainMap


logger = logging.getLogger(__name__)

DEFAULT_ASSETS_DIR = os.path.join(__package__ or 'wazo_acceptance', 'assets')
DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.wazo-acceptance')

DEFAULT_INSTANCE_CONFIG = {
    'master_host': None,
    'slave_host': None,
    'default_tenant': 'wazo-tenant',
    'log_file': '/tmp/wazo-acceptance.log',
    'assets_dir': DEFAULT_ASSETS_DIR,
    'agentd': {
        'verify_certificate': False,
    },
    'amid': {
        'verify_certificate': False,
    },
    'auth': {
        'verify_certificate': False,
    },
    'call_logd': {
        'verify_certificate': False,
    },
    'calld': {
        'verify_certificate': False,
    },
    'confd': {
        'verify_certificate': False,
    },
    'dird': {
        'verify_certificate': False,
    },
    'provd': {
        'verify_certificate': False,
    },
    'setupd': {
        'verify_certificate': False,
    },
    'websocketd': {
        'verify_certificate': False,
    },
    'ssh_login': 'root',
    'linphone': {
        'sip_port_range': '5001,5009',
        'rtp_port_range': '5100,5120',
    },
    'debug': {
        'global': False,

        'acceptance': False,
        'linphone': False,
    },
    'bus': {
        'exchange_name': 'xivo',
        'exchange_type': 'topic',
        'exchange_durable': True,
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
    },
    'prerequisites': {
        'subnets': [
            '10.0.0.0/8',
            '192.168.0.0/16',
        ]
    }
}


def load_config(config_dir=None):
    config_dir = config_dir or DEFAULT_CONFIG_DIR
    config_dir = os.path.abspath(config_dir)
    logger.debug('Reading config from %s...', config_dir)
    file_configs = parse_config_dir(config_dir)
    config = ChainMap(*file_configs)

    # set default config for each instance
    config = {instance: ChainMap(config[instance], deepcopy(DEFAULT_INSTANCE_CONFIG)) for instance in config}

    for instance_config in config.values():
        _config_update_host(instance_config)
        _config_post_processor(instance_config)

    return config


def _config_post_processor(config):
    if 'db_uri' not in config:
        config['db_uri'] = 'postgresql://asterisk:proformatique@{}/asterisk'.format(config['wazo_host'])
    config['bus_url'] = 'amqp://{username}:{password}@{host}:{port}//'.format(**config['bus'])


def _config_update_host(config):
    wazo_host = config.get('wazo_host')
    if not wazo_host:
        raise Exception('wazo_host key must be defined')

    services = (
        'agentd',
        'amid',
        'auth',
        'call_logd',
        'calld',
        'confd',
        'dird',
        'provd',
        'setupd',
        'bus',
        'websocketd',
    )
    for service in services:
        config[service].setdefault('host', wazo_host)
