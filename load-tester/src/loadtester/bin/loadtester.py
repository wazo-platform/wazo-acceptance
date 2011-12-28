# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import argparse
import logging
from loadtester import core
from loadtester.bin import commands


def main():
    _init_logging()
    commands.execute_command(_LoadtesterCommand())


def _init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)


class _LoadtesterCommand(object):
    def __init__(self):
        self._init_subcommands()

    def _init_subcommands(self):
        self._subcommands = commands.Subcommands()
        self._subcommands.add_subcommand(_AttachSubcommand('attach'))
        self._subcommands.add_subcommand(_StartSubcommand('start'))
        self._subcommands.add_subcommand(_StatusSubcommand('status'))

    def new_parser(self):
        parser = argparse.ArgumentParser()
        self._configure_parser(parser)
        self._subcommands.configure_parser(parser)
        return parser

    def _configure_parser(self, parser):
        parser.add_argument("-v", "--verbose", action="store_true", default=False,
                            help="increase logging verbosity")

    def execute(self, parsed_args):
        self._process_parsed_args(parsed_args)
        self._subcommands.execute(parsed_args)

    def _process_parsed_args(self, parsed_args):
        if parsed_args.verbose:
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)


class _AttachSubcommand(commands.AbstractSubcommand):
    def configure_parser(self, parser):
        parser.add_argument("scenario_dir", nargs="?",
                            help="path to the scenario directory")

    def execute(self, parsed_args):
        if parsed_args.scenario_dir:
            core.attach_to_scenario(parsed_args.scenario_dir)
        else:
            core.attach_to_first_scenario()


class _StartSubcommand(commands.AbstractSubcommand):
    def configure_parser(self, parser):
        parser.add_argument("scenario_dir",
                            help="path to the scenario directory")

    def execute(self, parsed_args):
        core.start_scenario(parsed_args.scenario_dir)


class _StatusSubcommand(commands.AbstractSubcommand):
    def execute(self, parsed_args):
        scenarios = core.list_running_scenarios()
        if scenarios:
            print "%s tests running" % (len(scenarios))
            for session in sorted(scenarios):
                print "    %s" % session
        else:
            print "No test running"


if __name__ == "__main__":
    main()
