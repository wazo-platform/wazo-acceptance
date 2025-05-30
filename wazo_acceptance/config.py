# Copyright 2014-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
from copy import deepcopy

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_dir

logger = logging.getLogger(__name__)

DEFAULT_ASSETS_DIR = os.path.join(__package__ or 'wazo_acceptance', 'assets')
DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.wazo-acceptance')

DEFAULT_GLOBAL_CONFIG = {
    'log_file': '/tmp/wazo-acceptance.log',
    'debug': {
        'global': False,

        'linphone': False,
        'wazo_acceptance': False,
        'wazo_test_helpers': False,
        'wazo_websocketd_client': False,
    },
    'instances': {}
}
DEFAULT_INSTANCE_CONFIG = {
    'master_host': None,
    'slave_host': None,
    'default_tenant': 'wazo-tenant',
    'assets_dir': DEFAULT_ASSETS_DIR,
    'agentd': {
        'verify_certificate': False,
    },
    'amid': {
        'verify_certificate': False,
    },
    'ari': {
        'username': 'xivo',
        'password': 'Nasheow8Eag',
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
    'chatd': {
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
    'ssh': {
        'login': 'root',
    },
    'linphone': {
        'sip_port_range': '5001,5009',
        'rtp_port_range': '5100,5120',
    },
    'bus': {
        'exchange_name': 'xivo',
        'exchange_type': 'topic',
        'exchange_durable': True,
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
    },
    'nat': {
        'local_net': None,
        'external_ip': None,
    },
    'system_password': None,
    'reload_timeout': 5,
    'sngrep': True,
    'tcpdump': False,
}


def load_config(config_dir=None):
    config_dir = config_dir or DEFAULT_CONFIG_DIR
    config_dir = os.path.abspath(config_dir)
    logger.debug('Reading config from %s...', config_dir)
    file_configs = parse_config_dir(config_dir)
    config = ChainMap(*file_configs, DEFAULT_GLOBAL_CONFIG)
    instances = config['instances']

    if not instances:
        raise Exception('At least one instance should be defined. See the README for the format.')

    # set default config for each instance
    instances = {instance: ChainMap(instances[instance], deepcopy(DEFAULT_INSTANCE_CONFIG))
                 for instance in instances}

    for instance_config in instances.values():
        _config_update_host(instance_config)
        _config_post_processor(instance_config)

    config['instances'] = instances
    return config


def _config_post_processor(config):
    if 'db_uri' not in config:
        config['db_uri'] = f'postgresql://asterisk:proformatique@{config["wazo_host"]}/asterisk'
    config['bus_url'] = 'amqp://{username}:{password}@{host}:{port}//'.format(**config['bus'])


def _config_update_host(config):
    wazo_host = config.get('wazo_host')
    if not wazo_host:
        raise Exception('wazo_host key must be defined')

    services = (
        'agentd',
        'amid',
        'auth',
        'ari',
        'call_logd',
        'calld',
        'chatd',
        'confd',
        'dird',
        'provd',
        'setupd',
        'ssh',
        'bus',
        'websocketd',
    )
    for service in services:
        config[service].setdefault('host', wazo_host)

    # Useful when HTTP are proxied by not provisioning server
    config['provd'].setdefault('provisioning_host', wazo_host)

    ari_host = config['ari'].pop('host')
    config['ari']['base_url'] = f"http://{ari_host}:5039"
