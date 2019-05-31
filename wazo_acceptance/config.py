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

DEFAULT_WAZO_HOST = os.environ.get('WAZO_HOST', 'daily-wazo-rolling-dev.lan.wazo.io')

DEFAULT_INSTANCE_CONFIG = {
    'wazo_host': DEFAULT_WAZO_HOST,
    'master_host': None,
    'slave_host': None,
    'default_tenant': 'wazo-tenant',
    'log_file': '/tmp/wazo-acceptance.log',
    'assets_dir': DEFAULT_ASSETS_DIR,
    'agentd': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'amid': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'auth': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'call_logd': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'calld': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'confd': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'dird': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'provd': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
    },
    'setupd': {
        'host': DEFAULT_WAZO_HOST,
        'verify_certificate': False,
        'timeout': 60,
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
        'host': DEFAULT_WAZO_HOST,
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


def load_config(extra_config_dir=None):
    extra_configs = []
    if extra_config_dir:
        extra_configs = parse_config_dir(extra_config_dir)
    file_configs = parse_config_dir(DEFAULT_CONFIG_DIR)
    config = ChainMap(*extra_configs, *file_configs)

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
        'bus'
    )
    for service in services:
        if config[service]['host'] == DEFAULT_WAZO_HOST:
            config[service]['host'] = config['wazo_host']
