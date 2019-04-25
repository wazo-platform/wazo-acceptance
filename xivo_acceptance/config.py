# -*- coding: utf-8 -*-
# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import print_function

import logging
import os
import sys

import yaml
import xivo_dao

from xivo_acceptance.lettuce import ssh


logger = logging.getLogger(__name__)

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CONFIG_DIRS = [
    os.getenv('LETTUCE_CONFIG', 'invalid_lettuce_config'),
    os.path.join(os.path.expanduser("~"), '.xivo-acceptance'),
    os.path.join(_ROOT_DIR, 'config')
]
_ASSETS_DIRS = [
    '/usr/share/xivo-acceptance/assets',
    os.path.join(sys.prefix, 'share', 'xivo-acceptance', 'assets'),
    os.path.join(_ROOT_DIR, 'data', 'assets')
]
_FEATURES_DIRS = [
    '/usr/share/xivo-acceptance/features',
    os.path.join(sys.prefix, 'share', 'xivo-acceptance', 'features'),
    os.path.join(_ROOT_DIR, 'data', 'features')
]

DEFAULT_XIVO_HOST = 'daily-xivo-pxe.lan.wazo.io'


def load_config(extra_config):
    config = {
        'xivo_host': DEFAULT_XIVO_HOST,
        'master_host': None,
        'slave_host': None,
        'log_file': '/tmp/xivo-acceptance.log',
        'assets_dir': _find_first_existing_path(_ASSETS_DIRS),
        'features_dir': _find_first_existing_path(_FEATURES_DIRS),
        'output_dir': '/tmp',
        'auth': {
            'host': DEFAULT_XIVO_HOST,
            'verify_certificate': False
        },
        'amid': {
            'host': DEFAULT_XIVO_HOST,
            'port': 9491,
            'https': True,
            'verify_certificate': False
        },
        'call_logd': {
            'host': DEFAULT_XIVO_HOST,
            'port': 9298,
            'https': True,
            'verify_certificate': False
        },
        'confd': {
            'host': DEFAULT_XIVO_HOST,
            'port': 9486,
            'https': True,
            'verify_certificate': False
        },
        'ctid_ng': {
            'host': DEFAULT_XIVO_HOST,
            'port': 9500,
            'https': True,
            'verify_certificate': False
        },
        'dird': {
            'host': DEFAULT_XIVO_HOST,
            'port': 9489,
            'https': True,
            'verify_certificate': False
        },
        'provd': {
            'host': DEFAULT_XIVO_HOST,
            'port': 8666,
            'https': True,
            'verify_certificate': False,
            'prefix': '/provd',
        },
        'setupd': {
            'host': DEFAULT_XIVO_HOST,
            'verify_certificate': False,
            'timeout': 60,
        },
        'ssh_login': 'root',
        'linphone': {
            'sip_port_range': '5001,5009',
            'rtp_port_range': '5100,5120'
        },
        'debug': {
            'acceptance': False,
            'global': False,
            'linphone': False,
        },
        'bus': {
            'exchange_name': 'xivo',
            'exchange_type': 'topic',
            'exchange_durable': True,
            'host': DEFAULT_XIVO_HOST,
            'port': 5672,
            'username': 'guest',
            'password': 'guest',
        },
        'prerequisites': {
            'subnets': [
                '10.0.0.0/8',
                '192.168.0.0/16'
            ]
        }
    }

    if extra_config:
        try:
            extra_config_file_path = _find_first_existing_path(_CONFIG_DIRS, file_name=extra_config)
            print('Using extra configuration file {}'.format(extra_config_file_path))
            config.update(_parse_config_file(extra_config_file_path))
        except Exception as e:
            print(e)

    host_from_env = os.environ.get('XIVO_HOST')
    if host_from_env:
        config['xivo_host'] = host_from_env

    _config_update_host(config)
    _config_post_processor(config)

    return config


def _config_post_processor(config):
    if 'db_uri' not in config:
        config['db_uri'] = 'postgresql://asterisk:proformatique@{}/asterisk'.format(config['xivo_host'])
    config['bus_url'] = 'amqp://{username}:{password}@{host}:{port}//'.format(**config['bus'])


def _config_update_host(config):
    if config['auth']['host'] == DEFAULT_XIVO_HOST:
        config['auth']['host'] = config['xivo_host']

    if config['amid']['host'] == DEFAULT_XIVO_HOST:
        config['amid']['host'] = config['xivo_host']

    if config['call_logd']['host'] == DEFAULT_XIVO_HOST:
        config['call_logd']['host'] = config['xivo_host']

    if config['confd']['host'] == DEFAULT_XIVO_HOST:
        config['confd']['host'] = config['xivo_host']

    if config['ctid_ng']['host'] == DEFAULT_XIVO_HOST:
        config['ctid_ng']['host'] = config['xivo_host']

    if config['dird']['host'] == DEFAULT_XIVO_HOST:
        config['dird']['host'] = config['xivo_host']

    if config['setupd']['host'] == DEFAULT_XIVO_HOST:
        config['setupd']['host'] = config['xivo_host']

    if config['bus']['host'] == DEFAULT_XIVO_HOST:
        config['bus']['host'] = config['xivo_host']


def _parse_config_file(config_file_name):
    try:
        with open(config_file_name) as config_file:
            return yaml.load(config_file)
    except IOError as e:
        print('Could not read config file {}: {}'.format(config_file_name, e), file=sys.stderr)
        return {}


def _find_first_existing_path(paths, file_name=None):
    for path in paths:
        if file_name:
            path = os.path.join(path, file_name)
        if os.path.exists(path):
            return path
    raise Exception('Path does not exist: %s' % ' '.join(paths))


class XivoAcceptanceConfig(object):

    def __init__(self, config):
        self._config = config
        logger.debug("_setup_dao...")
        self._setup_dao()
        logger.debug("_setup_ssh_client...")
        self._setup_ssh_client()

    def _setup_dao(self):
        xivo_dao.init_db(self._config['db_uri'])

    def _setup_ssh_client(self):
        self.ssh_client_xivo = ssh.SSHClient(hostname=self._config['xivo_host'],
                                             login=self._config['ssh_login'])
