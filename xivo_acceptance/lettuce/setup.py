# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from lettuce import world

from xivo_agentd_client import Client as AgentdClient
from xivo_auth_client import Client as AuthClient
from wazo_call_logd_client import Client as CallLogdClient
from xivo_confd_client import Client as ConfdClient
from xivo_ctid_ng_client import Client as CtidNgClient
from xivo_dird_client import Client as DirdClient

from xivo_acceptance.helpers import entity_helper

from . import auth
from . import debug
from ..config import load_config, XivoAcceptanceConfig
from .display import XiVODisplay
from .xivobrowser import XiVOBrowser

logger = logging.getLogger(__name__)


def setup_agentd_client():
    world.agentd_client = AgentdClient(world.config['xivo_host'],
                                       token=world.config['auth_token'],
                                       verify_certificate=False)
    auth.register_for_token_renewal(world.agentd_client.set_token)


def setup_call_logd_client():
    world.call_logd_client = CallLogdClient(**world.config['call_logd'])
    world.call_logd_client.set_token(world.config.get('auth_token'))
    auth.register_for_token_renewal(world.call_logd_client.set_token)


def setup_confd_client():
    world.confd_client = ConfdClient(**world.config['confd'])
    world.confd_client.set_token(world.config.get('auth_token'))
    auth.register_for_token_renewal(world.confd_client.set_token)


def setup_ctid_ng_client():
    world.ctid_ng_client = CtidNgClient(**world.config['ctid_ng'])
    world.ctid_ng_client.set_token(world.config.get('auth_token'))
    auth.register_for_token_renewal(world.ctid_ng_client.set_token)


def setup_dird_client():
    world.dird_client = DirdClient(**world.config['dird'])
    world.dird_client.set_token(world.config.get('auth_token'))
    auth.register_for_token_renewal(world.dird_client.set_token)


def setup_auth_token():
    world.auth_client = AuthClient(world.config['xivo_host'],
                                   username='xivo-acceptance',
                                   password='proformatique',
                                   verify_certificate=False)
    world.config['auth_token'] = auth.new_auth_token()
    world.auth_client.set_token(world.config.get('auth_token'))
    auth.register_for_token_renewal(world.auth_client.set_token)


def setup_tenant():
    entity_name = world.config.get('entity')
    if entity_name:
        entity = entity_helper.get_entity_with_name(entity_name)
    else:
        try:
            entity = entity_helper.get_default_entity()
        except Exception:
            logger.exception('failed to get an entity')
            return

    if not entity:
        return

    tenant_uuid = entity['tenant']['uuid']

    world.auth_client.set_tenant(tenant_uuid)
    world.confd_client.set_tenant(tenant_uuid)


@debug.logcall
def setup_browser():
    world.browser = XiVOBrowser(world.config['debug']['selenium'])


def setup_display():
    world.display = XiVODisplay()


def setup_config(extra_config):
    world.config = load_config(extra_config)


def setup_consul():
    command = 'cat /var/lib/consul/master_token'.split()
    world.config['consul_token'] = world.ssh_client_xivo.out_call(command).strip()


def setup_logging():
    debug.setup_logging(world.config)


@debug.logcall
def setup_provd():
    world.rest_provd = world.xivo_acceptance_config.rest_provd
    world.provd_client = world.xivo_acceptance_config.provd_client


@debug.logcall
def setup_ssh_client():
    world.ssh_client_xivo = world.xivo_acceptance_config.ssh_client_xivo


def setup_xivo_acceptance_config():
    world.xivo_acceptance_config = XivoAcceptanceConfig(world.config)


@debug.logcall
def setup_ws():
    # Prerequisite:
    # - setup_xivo_acceptance_config
    world.ws = world.xivo_acceptance_config.ws_utils


@debug.logcall
def teardown_browser():
    world.browser.quit()
    if hasattr(world, 'display'):
        world.display.get_instance().stop()


def setup_xivo_configured():
    try:
        world.xivo_configured = world.confd_client.wizard.get()['configured']
    except Exception:
        world.xivo_configured = False
