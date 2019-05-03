# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
import signal
import ssl

from xivo.xivo_logging import setup_logging

from .config import load_config
from .service import prerequisite


logger = logging.getLogger(__name__)


def main():
    signal.signal(signal.SIGTERM, _handle_sigterm)
    _disable_ssl_cert_verification()
    parsed_args = _parse_args()

    config = load_config(extra_config=parsed_args.config)
    setup_logging(log_file=config['log_file'], foreground=True, debug=parsed_args.verbose)

    if parsed_args.prerequisite:
        prerequisite.run(parsed_args.config)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prerequisite', action='store_true', help='execute prerequisite')
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    parser.add_argument('-c', '--config', help='config file name (not the path)', default='default')
    return parser.parse_args()


def _disable_ssl_cert_verification():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def _handle_sigterm(signum, frame):
    raise SystemExit()
