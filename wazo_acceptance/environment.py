# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo.xivo_logging import setup_logging as wazo_setup_logging

from . import (
    debug,
    setup
)
from .config import load_config

logger = logging.getLogger('acceptance')


class Instances:
    '''Container for InstanceContext. Each attribute is an InstanceContext'''
    pass


class InstanceContext:
    '''Substitute for behave's context, one per instance'''

    def __init__(self, global_context):
        self._global_context = global_context

    def add_cleanup(self, *args, **kwargs):
        self._global_context.add_cleanup(*args, **kwargs)


# Implicitly defined by behave
def before_all(context):
    initialize(context)
    context.fail_on_cleanup_errors = False


# Implicitly defined by behave
def before_scenario(context, scenario):
    scenario.user_tokens = {}
    if 'no_cleanup_errors_fail' not in context.tags:
        with context._use_with_behave_mode():
            context.fail_on_cleanup_errors = True


# Implicitly defined by behave
def after_scenario(context, scenario):
    if hasattr(context, 'helpers'):
        context.helpers.asterisk.send_to_asterisk_cli('channel request hangup all')


def initialize(context):
    config = load_config(config_dir=context.config.userdata.get('acceptance_config_dir'))
    wazo_setup_logging(config['log_file'], foreground=True, debug=config['debug']['global'])
    debug.setup_logging(config['log_file'], config['debug'])

    if config['instances'].get('default'):
        set_wazo_instance(context, 'default', config['instances']['default'], config['debug'])
    set_wazo_instances(context, config['instances'], config['debug'])


def set_wazo_instances(context, instances_config, debug_config):
    context.instances = Instances()
    for instance_name, instance_config in instances_config.items():
        instance_context = InstanceContext(context)
        set_wazo_instance(instance_context, instance_name, instance_config, debug_config)
        context.instances.__setattr__(instance_name, instance_context)


def set_wazo_instance(context, instance_name, instance_config, debug_config):
    logger.info("Adding instance %s...", instance_name)
    setup.setup_config(context, instance_config)

    logger.info('wazo_host: %s', context.wazo_config['wazo_host'])

    logger.debug("setup ssh client...")
    setup.setup_ssh_client(context)
    logger.debug("setup auth token...")
    setup.setup_auth_token(context)
    logger.debug("setup amid client...")
    setup.setup_amid_client(context)
    logger.debug("setup agentd client...")
    setup.setup_agentd_client(context)
    logger.debug("setup call logd client...")
    setup.setup_call_logd_client(context)
    logger.debug("setup calld client...")
    setup.setup_calld_client(context)
    logger.debug("setup confd client...")
    setup.setup_confd_client(context)
    logger.debug("setup dird client...")
    setup.setup_dird_client(context)
    logger.debug("setup provd client...")
    setup.setup_provd_client(context)
    logger.debug("setup setupd client...")
    setup.setup_setupd_client(context)
    logger.debug("setup websocketd client...")
    setup.setup_websocketd_client(context)
    logger.debug("setup tenant...")
    setup.setup_tenant(context)
    logger.debug("setup consul...")
    setup.setup_consul(context)
    logger.debug("setup remote sysutils...")
    setup.setup_remote_sysutils(context)
    logger.debug("setup helpers...")
    setup.setup_helpers(context)
    logger.debug("setup phone...")
    setup.setup_phone(context, debug_config['linphone'])
