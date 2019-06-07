# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from requests.exceptions import HTTPError

from wazo_auth_client import Client as AuthClient
from wazo_call_logd_client import Client as CallLogdClient
from wazo_calld_client import Client as CalldClient
from wazo_confd_client import Client as ConfdClient
from wazo_dird_client import Client as DirdClient
from wazo_provd_client import Client as ProvdClient
from wazo_setupd_client import Client as SetupdClient
from xivo_agentd_client import Client as AgentdClient
from xivo_amid_client import Client as AmidClient

from . import auth
from . import debug
from .helpers.asset import AssetHelper
from .helpers.asterisk import AsteriskHelper
from .helpers.confd_group import ConfdGroupHelper
from .helpers.confd_user import ConfdUserHelper
from .helpers.conference import ConferenceHelper
from .helpers.context import ContextHelper
from .helpers.endpoint_sip import EndpointSIPHelper
from .helpers.extension import ExtensionHelper
from .helpers.line import LineHelper
from .helpers.token import TokenHelper
from .helpers.user import UserHelper
from .helpers.sip_config import SIPConfigGenerator
from .helpers.sip_phone import LineRegistrar
from .phone_register import PhoneRegister
from .ssh import SSHClient
from .sysutils import RemoteSysUtils

logger = logging.getLogger(__name__)


def setup_agentd_client(context):
    context.agentd_client = AgentdClient(**context.wazo_config['agentd'])
    context.agentd_client.set_token(context.token)
    auth.register_for_token_renewal(context.agentd_client.set_token)


def setup_amid_client(context):
    context.amid_client = AmidClient(**context.wazo_config['amid'])
    context.amid_client.set_token(context.token)
    auth.register_for_token_renewal(context.amid_client.set_token)


def setup_call_logd_client(context):
    context.call_logd_client = CallLogdClient(**context.wazo_config['call_logd'])
    context.call_logd_client.set_token(context.token)
    auth.register_for_token_renewal(context.call_logd_client.set_token)


def setup_confd_client(context):
    context.confd_client = ConfdClient(**context.wazo_config['confd'])
    context.confd_client.set_token(context.token)
    auth.register_for_token_renewal(context.confd_client.set_token)


def setup_calld_client(context):
    context.calld_client = CalldClient(**context.wazo_config['calld'])
    context.calld_client.set_token(context.token)
    auth.register_for_token_renewal(context.calld_client.set_token)


def setup_dird_client(context):
    context.dird_client = DirdClient(**context.wazo_config['dird'])
    context.dird_client.set_token(context.token)
    auth.register_for_token_renewal(context.dird_client.set_token)


def setup_auth_token(context):
    context.auth_client = AuthClient(
        username='wazo-acceptance',
        password='hidden',
        **context.wazo_config['auth']
    )
    context.token = auth.new_auth_token(context)
    context.auth_client.set_token(context.token)
    auth.register_for_token_renewal(context.auth_client.set_token)


def setup_provd_client(context):
    context.provd_client = ProvdClient(**context.wazo_config['provd'])
    context.provd_client.set_token(context.token)
    auth.register_for_token_renewal(context.provd_client.set_token)


def setup_setupd_client(context):
    context.setupd_client = SetupdClient(**context.wazo_config['setupd'])
    context.setupd_client.set_token(context.token)
    auth.register_for_token_renewal(context.setupd_client.set_token)


def setup_tenant(context):
    name = context.wazo_config['default_tenant']
    try:
        tenants = context.auth_client.tenants.list(name=name)['items']
    except HTTPError:
        logger.exception('Error or Unauthorized to list tenants')
        return

    if not tenants:
        logger.exception('failed to get default tenant')
        return

    context.auth_client.set_tenant(tenants[0]['uuid'])
    context.confd_client.set_tenant(tenants[0]['uuid'])


def setup_config(context, config):
    context.wazo_config = config


def setup_consul(context):
    command = 'cat /var/lib/consul/master_token'.split()
    context.wazo_config['consul_token'] = context.ssh_client.out_call(command).strip()


@debug.logcall
def setup_ssh_client(context):
    context.ssh_client = SSHClient(
        hostname=context.wazo_config['wazo_host'],
        login=context.wazo_config['ssh_login'],
    )


class Helpers:
    pass


def setup_helpers(context):
    context.helpers = Helpers()
    context.helpers.asset = AssetHelper(context)
    context.helpers.asterisk = AsteriskHelper(context.ssh_client)
    context.helpers.confd_group = ConfdGroupHelper(context)
    context.helpers.confd_user = ConfdUserHelper(context)
    context.helpers.conference = ConferenceHelper(context)
    context.helpers.context = ContextHelper(context.confd_client)
    context.helpers.endpoint_sip = EndpointSIPHelper(context)
    context.helpers.extension = ExtensionHelper(context)
    context.helpers.line = LineHelper(context)
    context.helpers.token = TokenHelper(context)
    context.helpers.user = UserHelper(context)


def setup_remote_sysutils(context):
    context.remote_sysutils = RemoteSysUtils(context.ssh_client)


def setup_phone(context):
    context.phone_register = PhoneRegister(context.amid_client)
    context.helpers.sip_phone = LineRegistrar(context.wazo_config['debug'].get('linphone', False))
    context.helpers.sip_config = SIPConfigGenerator(
        context.wazo_config['wazo_host'],
        context.wazo_config['linphone'],
        context.phone_register,
    )
