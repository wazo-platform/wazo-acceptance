# -*- coding: UTF-8 -*-

import argparse
import mock
import sys
import unittest
from loadtester.bin.commands import AbstractSubcommand, Subcommands, \
    CommandExecutor, AbstractCommand, execute_command


def _new_parser():
    return argparse.ArgumentParser()


def _first_call_args(mock):
    return mock.call_args[0][0]


class TestExecuteCommand(unittest.TestCase):
    def setUp(self):
        self.mock_parser = mock.Mock()
        self.mock_parser.parse_args.return_value = mock.sentinel.ReturnValue
        self.mock_command = mock.Mock()
        self.mock_command.new_parser.return_value = self.mock_parser

    def test_command_is_called_with_args_when_args_given(self):
        args = ['foo']
        execute_command(self.mock_command, args)

        self.mock_parser.parse_args.assert_called_once_with(args)
        self.mock_command.execute.assert_called_once_with(mock.sentinel.ReturnValue)

    def test_command_is_called_with_sys_argv_when_args_not_given(self):
        execute_command(self.mock_command)

        self.mock_parser.parse_args.assert_called_once_with(sys.argv[1:])
        self.mock_command.execute.assert_called_once_with(mock.sentinel.ReturnValue)


class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        self.mock_command = mock.Mock()
        self.command_executor = CommandExecutor(self.mock_command)

    def test_execute_calls_command_new_parser(self):
        self.mock_command.new_parser.return_value = argparse.ArgumentParser()

        self.command_executor.execute([])

        self.assertTrue(self.mock_command.new_parser.called)

    def test_execute_calls_command_execute(self):
        parser = _new_parser()
        parser.add_argument('foo')
        self.mock_command.new_parser.return_value = parser

        self.command_executor.execute(['bar'])

        self.assertTrue(self.mock_command.execute.called)
        self.assertEqual('bar', _first_call_args(self.mock_command.execute).foo)


class TestAbstractCommand(unittest.TestCase):
    def setUp(self):
        self.command = AbstractCommand()

    def test_new_parser_returns_argument_parser(self):
        parser = self.command.new_parser()

        self.assertTrue(isinstance(parser, argparse.ArgumentParser))


class TestSubcommands(unittest.TestCase):
    def setUp(self):
        self.subcommands = Subcommands()

    def test_add_subcommand_appends_element_to_list(self):
        self.subcommands.add_subcommand(mock.sentinel.Arg)

        self.assertEqual([mock.sentinel.Arg], self.subcommands._subcommands)

    def test_configure_parser_calls_subcommands_configure_parser(self):
        foo_subcommand = self._new_mock_subcommand('foo')

        self.subcommands.add_subcommand(foo_subcommand)
        self.subcommands.configure_parser(_new_parser())

        self.assertTrue(foo_subcommand.configure_parser.called)
        self.assertTrue(isinstance(_first_call_args(foo_subcommand.configure_parser),
                                   argparse.ArgumentParser))

    def _new_mock_subcommand(self, name):
        mock_subcommand = mock.Mock()
        mock_subcommand.name = name
        return mock_subcommand

    def test_execute_calls_subcommand_execute_with_one_subcommand(self):
        foo_subcommand = self._new_mock_subcommand('foo')
        parser = _new_parser()

        self.subcommands.add_subcommand(foo_subcommand)
        self.subcommands.configure_parser(parser)
        parsed_args = parser.parse_args(['foo'])
        self.subcommands.execute(parsed_args)

        foo_subcommand.execute.assert_called_once_with(parsed_args)

    def test_execute_calls_subcommand_execute_with_two_subcommands(self):
        foo_subcommand = self._new_mock_subcommand('foo')
        bar_subcommand = self._new_mock_subcommand('bar')
        parser = _new_parser()

        self.subcommands.add_subcommand(foo_subcommand)
        self.subcommands.add_subcommand(bar_subcommand)
        self.subcommands.configure_parser(parser)
        parsed_args = parser.parse_args(['bar'])
        self.subcommands.execute(parsed_args)

        bar_subcommand.execute.assert_called_once_with(parsed_args)
        self.assertFalse(foo_subcommand.execute.called)


class TestAbstractSubcommand(unittest.TestCase):
    NAME = 'foo'

    def setUp(self):
        self.subcommand = AbstractSubcommand(self.NAME)

    def test_name_attribute_is_the_same_as_constructor(self):
        self.assertEqual(self.NAME, self.subcommand.name)

    def test_configure_parser_does_nothing(self):
        parser_mock = mock.Mock()

        self.subcommand.configure_parser(parser_mock)

        self.assertEqual([], parser_mock.method_calls)
