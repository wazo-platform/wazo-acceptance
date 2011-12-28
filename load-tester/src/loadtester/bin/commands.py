# -*- coding: UTF-8 -*-

import argparse
import sys


def execute_command(command, args=None):
    if args is None:
        args = sys.argv[1:]
    command_executor = CommandExecutor(command)
    command_executor.execute(args)


class CommandExecutor(object):
    def __init__(self, command):
        self._command = command

    def execute(self, args):
        parser = self._command.new_parser()
        parsed_args = parser.parse_args(args)
        self._command.execute(parsed_args)


class AbstractCommand(object):
    def new_parser(self):
        return argparse.ArgumentParser()

    def execute(self, parsed_args):
        raise Exception('must be overriden in derived clas')


class Subcommands(object):
    def __init__(self):
        self._subcommands = []

    def add_subcommand(self, subcommand):
        self._subcommands.append(subcommand)

    def configure_parser(self, parser):
        subparsers = parser.add_subparsers()
        for subcommand in self._subcommands:
            subcommand_parser = subparsers.add_parser(subcommand.name)
            subcommand_parser.set_defaults(subcommand=subcommand)
            subcommand.configure_parser(subcommand_parser)

    def execute(self, parsed_args):
        subcommand = parsed_args.subcommand
        subcommand.execute(parsed_args)


class AbstractSubcommand(object):
    def __init__(self, name):
        self.name = name

    def configure_parser(self, parser):
        pass

    def execute(self, parsed_args):
        raise Exception('must be overriden in derived class')
