# -*- coding: UTF-8 -*-

from __future__ import absolute_import

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


class _LoadtesterCommand(commands.AbstractCommand):
    def configure_parser(self, parser):
        parser.add_argument("-v", "--verbose", action="store_true", default=False,
                            help="increase logging verbosity")

    def configure_subcommands(self, subcommands):
        subcommands.add_subcommand(_AttachSubcommand('attach'))
        subcommands.add_subcommand(_StartSubcommand('start'))
        subcommands.add_subcommand(_StatusSubcommand('status'))

    def pre_execute(self, parsed_args):
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
