# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from . import setup
from .assets import copy_asset_to_server

logger = logging.getLogger(__name__)


class Context:
    pass


def run(extra_config_dir):
    context = Context()
    logger.debug('Initializing ...')
    setup.setup_config(context, extra_config_dir)
    setup.setup_logging(context)
    setup.setup_ssh_client(context)

    logger.debug('Configuring remote sysutils')
    setup.setup_remote_sysutils(context)

    logger.debug('Configuring users external_api')
    _configure_auth_users(context)

    logger.debug('Creating auth client')
    setup.setup_auth_token(context)

    logger.debug('Configuring python clients')
    setup.setup_confd_client(context)

    logger.debug('Creating default tenant')
    _configure_default_tenant(context)

    logger.debug('Configuring python clients tenant')
    setup.setup_tenant(context)

    logger.debug('Configuring Consul')
    _configure_consul(context)

    logger.debug('Configuring RabbitMQ on Wazo')
    _configure_rabbitmq(context)

    logger.debug('Configuring xivo-agid on Wazo')
    _allow_agid_listen_on_all_interfaces(context)

    logger.debug('Installing chan_test (module for asterisk)')
    _install_chan_test(context)

    logger.debug('Installing core_dump program')
    _install_core_dump(context)

    logger.debug('Configuring helpers')
    setup.setup_helpers(context)

    logger.debug('Adding context')
    context.helpers.context.update_contextnumbers_user('default', 1000, 1999)
    context.helpers.context.update_contextnumbers_group('default', 2000, 2999)
    context.helpers.context.update_contextnumbers_queue('default', 3000, 3999)
    context.helpers.context.update_contextnumbers_conference('default', 4000, 4999)
    context.helpers.context.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

    logger.debug('Configuring wazo-auth')
    _configure_wazo_service(context, 'wazo-auth')

    logger.debug('Configuring xivo-amid')
    _configure_wazo_service(context, 'xivo-amid')

    logger.debug('Configuring xivo-confd')
    _configure_wazo_service(context, 'xivo-confd')

    logger.debug('Configuring wazo-calld')
    _configure_wazo_service(context, 'wazo-calld')

    logger.debug('Configuring wazo-dird')
    _configure_wazo_service(context, 'wazo-dird')


def _configure_rabbitmq(context):
    copy_asset_to_server(context, 'rabbitmq.config', '/etc/rabbitmq/rabbitmq.config')
    context.remote_sysutils.restart_service('rabbitmq-server')


def _configure_auth_users(context):
    _create_auth_user(
        context,
        username='wazo-acceptance',
        password='hidden',
        acl_templates=[
            'agentd.#',
            'amid.action.*.create',
            'auth.#',
            'call-logd.#',
            'calld.#',
            'confd.#',
            'dird.#',
            'provd.#',
        ],
    )


def _create_auth_user(context, username, password, acl_templates):
    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'create',
        '--password', password,
        '--purpose', 'external_api',
        username,
    ]
    user_uuid = context.ssh_client.out_call(cmd).strip()

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
    policy_uuid = context.ssh_client.out_call(cmd).strip()

    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'add',
        '--policy', policy_uuid,
        user_uuid,
    ]
    context.ssh_client.check_call(cmd)


def _configure_default_tenant(context):
    context.auth_client.tenants.new(name=context.wazo_config['default_tenant'])


def _add_line_to_remote_file(context, line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    context.ssh_client.check_call(command)


def _allow_agid_listen_on_all_interfaces(context):
    _add_line_to_remote_file(context, 'listen_address: 0.0.0.0', '/etc/xivo-agid/conf.d/acceptance.yml')


def _install_packages(context, packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    context.ssh_client.check_call(command)


def _install_chan_test(context):
    _install_packages(context, ['make', 'asterisk-dev', 'gcc', 'libc6-dev', 'libssl-dev'])
    command = ['rm', '-rf', '/usr/src/chan-test-master', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['wget', 'https://github.com/wazo-pbx/chan-test/archive/master.zip', '-O', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['unzip', '-d', '/usr/src', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master', 'install']
    context.ssh_client.check_call(command)


def _install_core_dump(context):
    copy_asset_to_server(context, 'core_dump.c', '/usr/src')
    _install_packages(context, ['gcc'])
    command = ['gcc', '-o', '/usr/local/bin/core_dump', '/usr/src/core_dump.c']
    context.ssh_client.check_call(command)


def _configure_consul(context):
    copy_asset_to_server(context, 'public_consul.json', '/etc/consul/xivo/public_consul.json')
    consul_pidfile = context.remote_sysutils.get_pidfile_for_service_name('consul')
    consul_is_running = context.remote_sysutils.is_process_running(consul_pidfile)
    if consul_is_running:
        context.remote_sysutils.restart_service('consul')


def _configure_wazo_service(context, service):
    _copy_daemon_config_file(context, service)
    service_pidfile = context.remote_sysutils.get_pidfile_for_service_name(service)
    service_is_running = context.remote_sysutils.is_process_running(service_pidfile)
    if service_is_running:
        context.remote_sysutils.restart_service(service)


def _copy_daemon_config_file(context, daemon_name):
    asset_filename = '{}-acceptance.yml'.format(daemon_name)
    remote_path = '/etc/{}/conf.d'.format(daemon_name)
    copy_asset_to_server(context, asset_filename, remote_path)