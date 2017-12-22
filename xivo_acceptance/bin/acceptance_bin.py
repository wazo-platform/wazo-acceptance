# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse
import logging
import signal
import ssl

from xivo.xivo_logging import setup_logging
from xivo_acceptance.config import load_config
from xivo_acceptance.controller import XiVOAcceptanceController
from xivo_acceptance.service.manager.feature_manager import FeatureManager


logger = logging.getLogger(__name__)


def main():
    _init_signal()
    _disable_ssl_cert_verification()
    parsed_args = _parse_args()

    config = load_config(extra_config=parsed_args.config)
    setup_logging(log_file=config['log_file'], foreground=True, debug=parsed_args.verbose)

    feature_manager = FeatureManager(config)

    controller = XiVOAcceptanceController(feature_manager=feature_manager)

    if parsed_args.prerequisite:
        controller.exec_prerequisite(extra_config=parsed_args.config)

    if parsed_args.internal_features:
        controller.internal_features(internal_features=parsed_args.internal_features)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--internal-features',
                        help='execute internal features')
    parser.add_argument('-p', '--prerequisite', action='store_true',
                        help='execute prerequisite')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="verbose mode")
    parser.add_argument('-c', '--config',
                        help='config file name (not the path)',
                        default='default')
    return parser.parse_args()


def _init_signal():
    signal.signal(signal.SIGTERM, _handle_sigterm)


def _disable_ssl_cert_verification():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def _handle_sigterm(signum, frame):
    raise SystemExit()
