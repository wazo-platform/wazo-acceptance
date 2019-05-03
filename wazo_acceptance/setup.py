# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from wazo_call_logd_client import Client as CallLogdClient
from wazo_calld_client import Client as CalldClient
from wazo_dird_client import Client as DirdClient
from wazo_provd_client import Client as ProvdClient
from wazo_setupd_client import Client as SetupdClient
from xivo_agentd_client import Client as AgentdClient
from xivo_amid_client import Client as AmidClient
from xivo_auth_client import Client as AuthClient
from xivo_confd_client import Client as ConfdClient

from . import auth
from . import debug
from .config import load_config, WazoAcceptanceConfig

logger = logging.getLogger(__name__)


def setup_agentd_client(context):
    context.agentd_client = AgentdClient(
        context.config['wazo_host'],
        token=context.config['auth_token'],
        verify_certificate=False,
    )
    auth.register_for_token_renewal(context.agentd_client.set_token)


def setup_amid_client(context):
    context.amid_client = AmidClient(**context.config['amid'])
    context.amid_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.amid_client.set_token)


def setup_call_logd_client(context):
    context.call_logd_client = CallLogdClient(**context.config['call_logd'])
    context.call_logd_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.call_logd_client.set_token)


def setup_confd_client(context):
    context.confd_client = ConfdClient(**context.config['confd'])
    context.confd_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.confd_client.set_token)


def setup_calld_client(context):
    context.calld_client = CalldClient(**context.config['calld'])
    context.calld_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.calld_client.set_token)


def setup_dird_client(context):
    context.dird_client = DirdClient(**context.config['dird'])
    context.dird_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.dird_client.set_token)


def setup_auth_token(context):
    context.auth_client = AuthClient(
        username='wazo-acceptance',
        password='hidden',
        **context.config['auth']
    )
    context.config['auth_token'] = auth.new_auth_token(context)
    context.auth_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.auth_client.set_token)


def setup_provd_client(context):
    context.provd_client = ProvdClient(**context.config['provd'])
    context.provd_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.provd_client.set_token)


def setup_setupd_client(context):
    context.setupd_client = SetupdClient(**context.config['setupd'])
    context.setupd_client.set_token(context.config.get('auth_token'))
    auth.register_for_token_renewal(context.setupd_client.set_token)


def setup_tenant(context):
    name = context.config['default_tenant']
    tenants = context.auth_client.tenants.list(name=name)['items']
    if not tenants:
        logger.exception('failed to get default tenant')
        return

    context.auth_client.set_tenant(tenants[0]['uuid'])
    context.confd_client.set_tenant(tenants[0]['uuid'])


def setup_config(context, extra_config):
    context.config = load_config(extra_config)


def setup_consul(context):
    command = 'cat /var/lib/consul/master_token'.split()
    context.config['consul_token'] = context.ssh_client.out_call(command).strip()


def setup_logging(context):
    debug.setup_logging(context.config)


@debug.logcall
def setup_ssh_client(context):
    context.ssh_client = context.wazo_acceptance_config.ssh_client


def setup_wazo_acceptance_config(context):
    context.wazo_acceptance_config = WazoAcceptanceConfig(context.config)
