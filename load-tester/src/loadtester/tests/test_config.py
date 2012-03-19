# -*- coding: UTF-8 -*-

import os.path
import unittest
from loadtester.config import ScenarioConfig


class TestScenarioConfig(unittest.TestCase):
    def test_simple_config(self):
        config_content = "a = 'a'\n"

        config = ScenarioConfig(config_content)

        self.assertEqual({'a': 'a'}, config.get_context_for_scenario('s1'))

    def test_config_with_undefined_name_raise_exception(self):
        config_content = "a = b\n"

        self.assertRaises(Exception, ScenarioConfig, config_content)

    def test_config_with_bad_syntax_raise_exception(self):
        config_content = "!a\n"

        self.assertRaises(Exception, ScenarioConfig, config_content)

    def test_new_from_filename(self):
        config_filename = os.path.join(os.path.dirname(__file__), 'config', 'example1')

        config = ScenarioConfig.new_from_filename(config_filename)

        self.assertEqual({'a': 'a'}, config.get_context_for_scenario('s1'))

    def test_config_using_scenarios_variable(self):
        config_content = """\
scenarios.s1.a = 's1.a'
"""

        config = ScenarioConfig(config_content)

        self.assertEqual({'a': 's1.a'}, config.get_context_for_scenario('s1'))

    def test_global_variables_doesnt_override_scenario_variable(self):
        config_content = """\
scenarios.s1.a = 's1.a'
a = 'a'
"""

        config = ScenarioConfig(config_content)

        self.assertEqual({'a': 's1.a'}, config.get_context_for_scenario('s1'))

    def test_hyphen_are_converted_to_underscore(self):
        config_content = "scenarios.s_1.a = 's_1.a'\n"

        config = ScenarioConfig(config_content)

        self.assertEqual({'a': 's_1.a'}, config.get_context_for_scenario('s-1'))
