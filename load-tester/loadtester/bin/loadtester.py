# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import argparse
import logging
import os.path
from loadtester.config import ScenarioConfig
from loadtester.runner import ScenarioRunner
from loadtester.scenario import Scenario

_CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../etc'))
_CONFIG_FILE = os.path.join(_CONFIG_DIR, 'conf.py')


def main():
    _init_logging()

    parsed_args = _parse_args()

    if parsed_args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    scenario_runner = ScenarioRunner()
    scenario = Scenario(parsed_args.scenario_dir)
    scenario_config = ScenarioConfig.new_from_filename(parsed_args.conf)
    scenario_runner.start_scenario(scenario, scenario_config)


def _init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase verbosity')
    parser.add_argument('-c', '--conf', default=_CONFIG_FILE,
                        help='path to the config file')
    parser.add_argument('scenario_dir',
                        help='path to the scenario directory')
    return parser.parse_args()


if __name__ == '__main__':
    main()
