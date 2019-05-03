# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo.xivo_logging import setup_logging as wazo_setup_logging

from . import asterisk
from . import setup
from .config import load_config
from .helpers import asterisk_helper
from .phone_register import PhoneRegister

logger = logging.getLogger('acceptance')


# Implicitly defined by behave
def before_all(context):
    initialize(context)


# Implicitly defined by behave
def before_scenario(context, scenario):
    scenario.phone_register = PhoneRegister(context)
    scenario.user_tokens = {}


# Implicitly defined by behave
def after_scenario(context, scenario):
    asterisk.stop_ami_monitoring()
    scenario.phone_register.clear()
    asterisk_helper.send_to_asterisk_cli(context, 'channel request hangup all')


def initialize(context, extra_config='default'):
    config = load_config(extra_config)
    debug = config.get('debug', {}).get('global', True)
    wazo_setup_logging(log_file=config['log_file'], foreground=True, debug=debug)
    set_wazo_target(context, extra_config)


def set_wazo_target(context, extra_config):
    setup.setup_config(context, extra_config)
    setup.setup_logging(context)

    logger.info("Initializing acceptance tests...")
    logger.info('wazo_host: %s', context.config['wazo_host'])

    setup.setup_wazo_acceptance_config(context)

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
    logger.debug("setup consul...")
    setup.setup_consul(context)
