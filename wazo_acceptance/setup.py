# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from requests.exceptions import HTTPError

from wazo_amid_client import Client as AmidClient
from wazo_agentd_client import Client as AgentdClient
from wazo_auth_client import Client as AuthClient
from wazo_call_logd_client import Client as CallLogdClient
from wazo_calld_client import Client as CalldClient
from wazo_chatd_client import Client as ChatdClient
from wazo_confd_client import Client as ConfdClient
from wazo_dird_client import Client as DirdClient
from wazo_provd_client import Client as ProvdClient
from wazo_setupd_client import Client as SetupdClient
from wazo_websocketd_client import Client as WebsocketdClient

from . import auth
from . import debug
from . import helpers
from .phone_register import PhoneRegister
from .ssh import SSHClient
from .sysutils import RemoteSysUtils

logger = logging.getLogger(__name__)


def setup_agentd_client(context):
    context.agentd_client = AgentdClient(**context.wazo_config['agentd'])
    context.agentd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.agentd_client.set_token)


def setup_amid_client(context):
    context.amid_client = AmidClient(**context.wazo_config['amid'])
    context.amid_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.amid_client.set_token)


def setup_call_logd_client(context):
    context.call_logd_client = CallLogdClient(**context.wazo_config['call_logd'])
    context.call_logd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.call_logd_client.set_token)


def setup_calld_client(context):
    context.calld_client = CalldClient(**context.wazo_config['calld'])
    context.calld_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.calld_client.set_token)


def setup_chatd_client(context):
    context.chatd_client = ChatdClient(**context.wazo_config['chatd'])
    context.chatd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.chatd_client.set_token)


def setup_confd_client(context):
    context.confd_client = ConfdClient(**context.wazo_config['confd'])
    context.confd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.confd_client.set_token)


def setup_dird_client(context):
    context.dird_client = DirdClient(**context.wazo_config['dird'])
    context.dird_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.dird_client.set_token)


def setup_auth_token(context):
    context.auth_client = AuthClient(
        username='wazo-acceptance',
        password='hidden',
        **context.wazo_config['auth']
    )
    context.token = auth.new_auth_token(context)
    context.auth_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.auth_client.set_token)


def setup_provd_client(context):
    context.provd_client = ProvdClient(**context.wazo_config['provd'])
    context.provd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.provd_client.set_token)


def setup_setupd_client(context):
    context.setupd_client = SetupdClient(**context.wazo_config['setupd'])
    context.setupd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.setupd_client.set_token)


def setup_websocketd_client(context):
    context.websocketd_client = WebsocketdClient(**context.wazo_config['websocketd'])
    context.websocketd_client.set_token(context.token)
    context.token_pubsub.subscribe('new-token-id', context.websocketd_client.set_token)


def setup_tenant(context):
    name = context.wazo_config['default_tenant']
    context.auth_client.set_tenant(None)
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
    context.helpers.agent = helpers.Agent(context)
    context.helpers.agent_skill = helpers.AgentSkill(context)
    context.helpers.application = helpers.Application(context)
    context.helpers.asset = helpers.Asset(context)
    context.helpers.asterisk = helpers.Asterisk(context.ssh_client)
    context.helpers.bus = helpers.Bus(context)
    context.helpers.call = helpers.Call(context)
    context.helpers.confd_group = helpers.ConfdGroup(context)
    context.helpers.confd_user = helpers.ConfdUser(context)
    context.helpers.conference = helpers.Conference(context)
    context.helpers.context = helpers.Context(context.confd_client)
    context.helpers.device = helpers.Device(context)
    context.helpers.endpoint_sip = helpers.EndpointSIP(context)
    context.helpers.extension = helpers.Extension(context)
    context.helpers.extension_feature = helpers.ExtensionFeature(context)
    context.helpers.incall = helpers.Incall(context)
    context.helpers.ivr = helpers.IVR(context)
    context.helpers.line = helpers.Line(context)
    context.helpers.monit = helpers.Monit(context)
    context.helpers.parking_lot = helpers.ParkingLot(context)
    context.helpers.pickup = helpers.Pickup(context)
    context.helpers.provd = helpers.Provd(context)
    context.helpers.queue = helpers.Queue(context)
    context.helpers.queue_skill_rule = helpers.QueueSkillRule(context)
    context.helpers.schedule = helpers.Schedule(context)
    context.helpers.token = helpers.Token(context)
    context.helpers.trunk = helpers.Trunk(context)
    context.helpers.user = helpers.User(context)
    context.helpers.voicemail = helpers.Voicemail(context)


def setup_remote_sysutils(context):
    context.remote_sysutils = RemoteSysUtils(context.ssh_client)


def setup_phone(context, linphone_debug):
    context.phone_register = PhoneRegister(context)
    context.helpers.sip_phone = helpers.PhoneFactory(context, linphone_debug)
    context.helpers.sip_config = helpers.SIPConfigGenerator(
        context.wazo_config['wazo_host'],
        context.wazo_config['linphone'],
        context.phone_register,
    )
