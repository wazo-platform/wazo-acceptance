# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
import signal

from xivo.xivo_logging import setup_logging

from . import prerequisite
from .config import load_config


logger = logging.getLogger(__name__)


def main():
    signal.signal(signal.SIGTERM, _handle_sigterm)
    parsed_args = _parse_args()

    config = load_config(config_dir=parsed_args.config)
    setup_logging(log_file=config['default']['log_file'], foreground=True, debug=parsed_args.verbose)

    if parsed_args.prerequisite:
        prerequisite.run(parsed_args.config, parsed_args.instance)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prerequisite', action='store_true', help='execute prerequisite')
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    parser.add_argument('-c', '--config', help='Config directory. Files must end with .yml')
    parser.add_argument('-i', '--instance', help='Name of the instance to target, as defined in config', default='default')
    return parser.parse_args()


def _handle_sigterm(signum, frame):
    raise SystemExit()
