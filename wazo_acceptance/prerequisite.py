# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

from requests.exceptions import HTTPError
from xivo.pubsub import Pubsub

from . import (
    debug,
    setup,
)
from .config import load_config

logger = logging.getLogger(__name__)

WAZO_SERVICES = [
    'wazo-agentd',
    'wazo-agid',
    'wazo-amid',
    'wazo-auth',
    'wazo-call-logd',
    'wazo-calld',
    'wazo-chatd',
    'wazo-confd',
    'wazo-confgend',
    'wazo-dird',
    'wazo-phoned',
    'wazo-plugind',
    'wazo-provd',
    'wazo-webhookd',
    'wazo-websocketd',
]


class Context:
    def __init__(self):
        self.token_pubsub = Pubsub()


def run(config_dir, instance_name):
    context = Context()

    logger.debug('Initializing ...')
    config = load_config(config_dir)
    instance_config = config['instances'][instance_name]
    setup.setup_config(context, instance_config)
    debug.setup_logging(config['log_file'], config['debug'])

    logger.debug('Running prerequisites for instance "%s" ...', instance_name)
    setup.setup_config(context, instance_config)

    setup.setup_ssh_client(context)

    logger.debug('Configuring remote sysutils')
    setup.setup_remote_sysutils(context)

    logger.debug('Configuring users external_api')
    _configure_auth_users(context)

    logger.debug('Creating auth client')
    setup.setup_auth_token(context)

    logger.debug('Configuring confd client')
    setup.setup_confd_client(context)

    logger.debug("Configuring websocketd client")
    setup.setup_websocketd_client(context)

    logger.debug("Configuring calld client")
    setup.setup_calld_client(context)

    logger.debug("Configuring call-logd client")
    setup.setup_call_logd_client(context)

    logger.debug("Configuring provd client")
    setup.setup_provd_client(context)

    logger.debug('Creating default tenant')
    _configure_default_tenant(context)

    logger.debug('Configuring python clients tenant')
    setup.setup_tenant(context)

    logger.debug('Configuring Consul')
    _configure_consul(context)

    logger.debug('Configuring RabbitMQ')
    _configure_rabbitmq(context)

    logger.debug('Configuring wazo-agid')
    _allow_agid_listen_on_all_interfaces(context)

    logger.debug('Installing chan_test (module for asterisk)')
    _install_chan_test(context)

    logger.debug('Installing wazo-crash-test program')
    _install_crash_test(context)

    logger.debug('Installing queue_log helpers')
    _install_queue_log_helpers(context)

    logger.debug('Configuring helpers')
    setup.setup_helpers(context)

    logger.debug('Adding instance context')
    context.helpers.context.update_contextnumbers_user('default', 1000, 1999)
    context.helpers.context.update_contextnumbers_group('default', 2000, 2999)
    context.helpers.context.update_contextnumbers_queue('default', 3000, 3999)
    context.helpers.context.update_contextnumbers_conference('default', 4000, 4999)
    context.helpers.context.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

    logger.debug('Configuring asterisk')
    _configure_asterisk(context)

    logger.debug('Configuring wazo services debugging...')
    _enable_wazo_services_debug(context)

    logger.debug('Configuring wazo-agid...')
    _configure_wazo_service(context, 'wazo-agid')

    logger.debug('Configuring postgresql debug')
    _configure_postgresql_debug(context)


def _configure_rabbitmq(context):
    copy_asset_to_server_permanently(context, 'rabbitmq.config', '/etc/rabbitmq')
    context.remote_sysutils.restart_service('rabbitmq-server')


def _configure_auth_users(context):
    if _auth_user_exists(context, 'wazo-acceptance'):
        return
    _create_auth_user(
        context,
        username='wazo-acceptance',
        password='hidden',
        acl=[
            'agentd.#',
            'amid.action.*.create',
            'auth.#',
            'call-logd.#',
            'calld.#',
            'confd.#',
            'dird.#',
            'provd.#',
            'events.#',
        ],
    )


def _auth_user_exists(context, username):
    cmd = [
        'wazo-auth-cli',
        '--config', '/root/.config/wazo-auth-cli',
        'user',
        'show',
        username,
    ]
    return_code = context.ssh_client.call(cmd)
    return return_code == 0


def _create_auth_user(context, username, password, acl):
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
    if acl:
        args = ['--acl']
        args.extend(acl)

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
    name = context.wazo_config['default_tenant']
    try:
        tenants = context.auth_client.tenants.list(name=name)['items']
    except HTTPError:
        logger.exception('Error or Unauthorized to list tenants')
        return
    if not tenants:
        context.auth_client.tenants.new(name=context.wazo_config['default_tenant'])


def _add_line_to_remote_file(context, line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    context.ssh_client.check_call(command)


def _allow_agid_listen_on_all_interfaces(context):
    _add_line_to_remote_file(context, 'listen_address: 0.0.0.0', '/etc/wazo-agid/conf.d/acceptance.yml')


def _install_packages(context, packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    context.ssh_client.check_call(command)


def _install_chan_test(context):
    _install_packages(context, ['make', 'asterisk-dev', 'gcc', 'libc6-dev', 'libssl-dev'])
    command = ['rm', '-rf', '/usr/src/chan-test-master', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['wget', 'https://github.com/wazo-platform/chan-test/archive/master.zip', '-O', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['unzip', '-d', '/usr/src', '/usr/src/chan-test.zip']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master']
    context.ssh_client.check_call(command)
    command = ['make', '-C', '/usr/src/chan-test-master', 'install']
    context.ssh_client.check_call(command)


def _install_crash_test(context):
    copy_asset_to_server_permanently(context, 'wazo-crash-test.c', '/usr/src')
    _install_packages(context, ['gcc'])
    command = ['gcc', '-o', '/usr/local/bin/wazo-crash-test', '/usr/src/wazo-crash-test.c']
    context.ssh_client.check_call(command)


def _install_queue_log_helpers(context):
    copy_asset_to_server_permanently(context, 'queue-log-clear-one-queue.sh', '/usr/local/bin')
    copy_asset_to_server_permanently(context, 'queue-log-count-queue-events.sh', '/usr/local/bin')
    copy_asset_to_server_permanently(context, 'queue-log-clear-one-agent.sh', '/usr/local/bin')
    copy_asset_to_server_permanently(context, 'queue-log-count-agent-events.sh', '/usr/local/bin')
    copy_asset_to_server_permanently(context, 'queue-log-insert-corrupt-entries.sh', '/usr/local/bin')


def _configure_consul(context):
    copy_asset_to_server_permanently(context, 'public_consul.json', '/etc/consul.d/zz-wazo-acceptance.json')
    consul_is_running = context.remote_sysutils.is_process_running('consul')
    if consul_is_running:
        context.remote_sysutils.restart_service('consul')


def _configure_asterisk(context):
    copy_asset_to_server_permanently(context, 'cli.conf', '/etc/asterisk/cli.conf')
    asterisk_is_running = context.remote_sysutils.is_process_running('asterisk')
    if asterisk_is_running:
        context.remote_sysutils.restart_service('asterisk')


def _configure_postgresql_debug(context):
    config_file = '/etc/postgresql/11/main/postgresql.conf'
    command = [
        'sed',
        '-i',
        '"s/#log_min_duration_statement = -1/log_min_duration_statement = 0/"',
        config_file,
    ]
    context.ssh_client.check_call(command)
    pg_is_running = context.remote_sysutils.is_process_running('postgresql@11-main')
    if pg_is_running:
        context.remote_sysutils.reload_service('postgresql')


def _enable_wazo_services_debug(context):
    for service in WAZO_SERVICES:
        logger.debug('Configuring %s debug', service)
        if service == 'wazo-provd':
            debug_content = 'general: {verbose: true}'
        else:
            debug_content = 'debug: true'
        command = ['echo', debug_content, '>', f'/etc/{service}/conf.d/wazo-acceptance-debug.yml']
        context.ssh_client.check_call(command)
        service_is_running = context.remote_sysutils.is_process_running(service)
        if service_is_running:
            context.remote_sysutils.restart_service(service)


def _configure_wazo_service(context, service):
    copy_asset_to_server_permanently(
        context,
        f'{service}.yml',
        f'/etc/{service}/conf.d/wazo-acceptance.yml',
    )
    service_is_running = context.remote_sysutils.is_process_running(service)
    if service_is_running:
        context.remote_sysutils.restart_service(service)


def copy_asset_to_server_permanently(context, asset, serverpath):
    assetpath = os.path.join(context.wazo_config['assets_dir'], asset)
    context.ssh_client.send_files(assetpath, serverpath)
