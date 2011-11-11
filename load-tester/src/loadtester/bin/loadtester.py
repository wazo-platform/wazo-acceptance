# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import argparse
import logging
import sys
from loadtester import core


def _new_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="increase logging verbosity")
    subparsers = parser.add_subparsers()

    parser_attach = subparsers.add_parser("attach")
    parser_attach.add_argument("scenario_dir", nargs="?",
                               help="path to the scenario directory")
    parser_attach.set_defaults(func=_action_attach)

    parser_start = subparsers.add_parser("start")
    parser_start.add_argument("scenario_dir",
                              help="path to the scenario directory")
    parser_start.set_defaults(func=_action_start)

    parser_status = subparsers.add_parser("status")
    parser_status.set_defaults(func=_action_status)

    return parser


def _init_logging(verbose=False):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)


def _parse_args(args):
    parser = _new_argument_parser()
    parsed_args = parser.parse_args(args)
    return parsed_args


def _action_attach(args):
    if args.scenario_dir:
        core.attach_to_scenario(args.scenario_dir)
    else:
        core.attach_to_first_scenario()


def _action_start(args):
    core.start_scenario(args.scenario_dir)


def _action_status(args):
    scenarios = core.list_running_scenarios()
    if scenarios:
        print "%s tests running" % (len(scenarios))
        for session in sorted(scenarios):
            print "    %s" % session
    else:
        print "No test running"


def main():
    args = _parse_args(sys.argv[1:])
    _init_logging(args.verbose)

    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
