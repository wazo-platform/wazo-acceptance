# -*- coding: UTF-8 -*-

import unittest
from loadtester import core


class TestExtractScenarioName(unittest.TestCase):
    def test_simple_dir(self):
        name = core._extract_scenario_name("foo")
        self.assertEqual("foo", name)

    def test_simple_dir_with_trailing_slash(self):
        name = core._extract_scenario_name("foo/")
        self.assertEqual("foo", name)

    def test_subdir(self):
        name = core._extract_scenario_name("scenarios/foo")
        self.assertEqual("foo", name)

    def test_subdir_with_trailing_slash(self):
        name = core._extract_scenario_name("scenarios/foo/")
        self.assertEqual("foo", name)
