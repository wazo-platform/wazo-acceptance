# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from lettuce import world

from xivo_acceptance.helpers import context_helper
from xivo_acceptance.lettuce import setup
from xivo_acceptance.lettuce import sysutils
from xivo_acceptance.lettuce.assets import copy_asset_to_server
from xivo_dao.helpers import db_manager
from xivo_dao.helpers.db_utils import session_scope


logger = logging.getLogger(__name__)


def run(extra_config):
    logger.debug('Initializing ...')
    setup.setup_config(extra_config)
    setup.setup_logging()
    setup.setup_xivo_acceptance_config()
    setup.setup_ssh_client()

    logger.debug('Configuring users external_api')
    _configure_auth_users()

    logger.debug('Creating auth client')
    setup.setup_auth_token()

    logger.debug('Configuring python clients')
    setup.setup_call_logd_client()
    setup.setup_confd_client()

    setup.setup_xivo_configured()

    logger.debug('Configuring CA certificates')
    _configure_ca_certificates()

    logger.debug('Configuring Consul')
    _configure_consul()

    logger.debug('Configuring PostgreSQL on XiVO')
    _configure_postgresql()

    logger.debug('Configuring RabbitMQ on XiVO')
    _configure_rabbitmq()

    logger.debug('Configuring xivo-agid on XiVO')
    _allow_agid_listen_on_all_interfaces()

    logger.debug('Configuring Provd REST API on XiVO')
    _allow_provd_listen_on_all_interfaces()

    logger.debug('Installing packages')
    _install_packages(['tcpflow'])

    logger.debug('Installing chan_test (module for asterisk)')
    _install_chan_test()

    logger.debug('Installing core_dump program')
    _install_core_dump()

    logger.debug('Adding context')
    context_helper.update_contextnumbers_queue('statscenter', 5000, 5100)
    context_helper.update_contextnumbers_user('statscenter', 1000, 1100)
    context_helper.update_contextnumbers_user('default', 1000, 1999)
    context_helper.update_contextnumbers_group('default', 2000, 2999)
    context_helper.update_contextnumbers_queue('default', 3000, 3999)
    context_helper.update_contextnumbers_meetme('default', 4000, 4999)
    context_helper.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

    logger.debug('Configuring wazo-auth')
    _configure_wazo_service('wazo-auth')

    logger.debug('Configuring xivo-amid')
    _configure_wazo_service('xivo-amid')

    logger.debug('Configuring xivo-confd')
    _configure_wazo_service('xivo-confd')

    logger.debug('Configuring xivo-ctid')
    _configure_wazo_service('xivo-ctid')

    logger.debug('Configuring xivo-ctid-ng')
    _configure_wazo_service('xivo-ctid-ng')


def _configure_postgresql():

    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)

    hba_file = '/etc/postgresql/9.6/main/pg_hba.conf'
    postgres_conf_file = '/etc/postgresql/9.6/main/postgresql.conf'

    subnet_line = 'host all all {subnet} md5'
    for subnet in world.config['prerequisites']['subnets']:
        _add_line_to_remote_file(subnet_line.format(subnet=subnet), hba_file)

    _add_line_to_remote_file("listen_addresses = '*'", postgres_conf_file)

    _restart_service('postgresql')
    db_manager.init_db(world.config['db_uri'])


def _configure_rabbitmq():
    copy_asset_to_server('rabbitmq.config', '/etc/rabbitmq/rabbitmq.config')
    _restart_service('rabbitmq-server')


def _configure_auth_users():
    _create_auth_user(
        'xivo-acceptance',
        'proformatique',
        [
            'amid.action.*.create',
            'auth.#',
            'confd.#',
            'dird.#',
            'agentd.#',
            'ctid-ng.#',
            'call-logd.#',
            'provd.#',
        ],
    )
    _create_auth_user(
        'admin',
        'proformatique',
        [],
    )


def _create_auth_user(username, password, acl_templates):
    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'create',
        '--password', password,
        '--purpose', 'external_api',
        username,
    ]
    user_uuid = world.ssh_client_xivo.out_call(cmd).decode('utf-8').strip()

    args = []
    if acl_templates:
        args = ['--acl']
        args.extend(acl_templates)

    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'policy',
        'create',
        '{}-policy'.format(username),
    ]
    cmd.extend(args)
    policy_uuid = world.ssh_client_xivo.out_call(cmd).decode('utf-8').strip()

    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'add',
        '--policy', policy_uuid,
        user_uuid,
    ]
    world.ssh_client_xivo.check_call(cmd)


def _add_line_to_remote_file(line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    world.ssh_client_xivo.check_call(command)


def _allow_agid_listen_on_all_interfaces():
    _add_line_to_remote_file('listen_address: 0.0.0.0', '/etc/xivo-agid/conf.d/acceptance.yml')


def _allow_provd_listen_on_all_interfaces():
    # TODO use REST API
    with session_scope() as session:
        query = 'UPDATE provisioning SET net4_ip_rest = \'0.0.0.0\''
        session.execute(query)
    # Apply common.conf


def _install_packages(packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    world.ssh_client_xivo.check_call(command)


def _install_chan_test():
    _install_packages(['make', 'asterisk-dev', 'gcc', 'libc6-dev', 'libssl-dev'])
    command = ['rm', '-rf', '/usr/src/chan-test-master', '/usr/src/chan-test.zip']
    world.ssh_client_xivo.check_call(command)
    command = ['wget', 'https://github.com/wazo-pbx/chan-test/archive/master.zip', '-O', '/usr/src/chan-test.zip']
    world.ssh_client_xivo.check_call(command)
    command = ['unzip', '-d', '/usr/src', '/usr/src/chan-test.zip']
    world.ssh_client_xivo.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master']
    world.ssh_client_xivo.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master', 'install']
    world.ssh_client_xivo.check_call(command)


def _install_core_dump():
    copy_asset_to_server('core_dump.c', '/usr/src')
    _install_packages(['gcc'])
    command = ['gcc', '-o', '/usr/local/bin/core_dump', '/usr/src/core_dump.c']
    world.ssh_client_xivo.check_call(command)


def _configure_ca_certificates():
    copy_asset_to_server('openldap-dev.crt', '/usr/local/share/ca-certificates')
    world.ssh_client_xivo.check_call(['update-ca-certificates'])


def _configure_consul():
    copy_asset_to_server('public_consul.json', '/etc/consul/xivo/public_consul.json')
    consul_is_running = sysutils.is_process_running(sysutils.get_pidfile_for_service_name('consul'))
    if consul_is_running:
        _restart_service('consul')


def _configure_wazo_service(service):
    _copy_daemon_config_file(service)
    service_is_running = sysutils.is_process_running(sysutils.get_pidfile_for_service_name(service))
    if service_is_running:
        _restart_service(service)


def _copy_daemon_config_file(daemon_name):
    asset_filename = '{}-acceptance.yml'.format(daemon_name)
    remote_path = '/etc/{}/conf.d'.format(daemon_name)
    copy_asset_to_server(asset_filename, remote_path)


def _restart_service(service_name):
    command = ['systemctl', 'restart', service_name]
    world.ssh_client_xivo.check_call(command)
