# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 Avencall
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

from xivo.xivo_logging import setup_logging
from xivo_acceptance.controller import XiVOAcceptanceController
from xivo_acceptance.service.manager.feature_manager import FeatureManager


logger = logging.getLogger(__name__)

_LOG_FILENAME = '/var/log/xivo-acceptance.log'


def main():
    _init_signal()
    parsed_args = _parse_args()
    setup_logging(log_file=_LOG_FILENAME, foreground=True, debug=parsed_args.verbose)

    feature_manager = FeatureManager()
    controller = XiVOAcceptanceController(feature_manager)

    if parsed_args.prerequisite:
        controller.exec_prerequisite()
    if parsed_args.feature:
        controller.exec_feature(feature=parsed_args.feature,
                                interactive=parsed_args.interactive)
    if parsed_args.acceptance_daily:
        controller.exec_acceptance_daily_features()
    if parsed_args.all:
        controller.exec_feature(feature=None,
                                interactive=parsed_args.interactive)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="  Default: %(default)s")
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='interactive mode')
    parser.add_argument('-p', '--prerequisite', action='store_true',
                        help='execute prerequisite')
    parser.add_argument('-a', '--all', action='store_true',
                        help='play all features')
    parser.add_argument('-d', '--acceptance-daily',
                        help='execute acceptance daily features')
    parser.add_argument('-f', '--feature',
                        help='feature name')
    return parser.parse_args()


def _init_signal():
    signal.signal(signal.SIGTERM, _handle_sigterm)


def _handle_sigterm(signum, frame):
    raise SystemExit()
