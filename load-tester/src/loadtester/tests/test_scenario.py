# -*- coding: UTF-8 -*-

import os
import shutil
import tempfile
import unittest
from loadtester.scenario import Scenario, _TemplatesProcessor


class TestScenario(unittest.TestCase):
    def test_scenario_name_from_simple_dir(self):
        scenario_src = Scenario('foo')

        self.assertEqual('foo', scenario_src.name)

    def test_scenario_name_from_simple_dir_with_trailing_slash(self):
        scenario_src = Scenario('foo/')

        self.assertEqual('foo', scenario_src.name)

    def test_scenario_name_from_subdir(self):
        scenario_src = Scenario('scenarios/foo')

        self.assertEqual('foo', scenario_src.name)

    def test_scenario_name_from_subdir_with_trailing_slash(self):
        scenario_src = Scenario('scenarios/foo/')

        self.assertEqual('foo', scenario_src.name)


class TestTemplatesProcessor(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_generate_files(self):
        # there's a bug in jinja2 causing it to eat the final newline
        #    https://github.com/mitsuhiko/jinja2/issues/75
        self._write_file('file1.tpl', 'Hi {{ name }}.\n\n')

        tpl_processor = self._new_tpl_processor({'name': 'James'})
        tpl_processor.generate_files()

        self.assertEqual('Hi James.\n', self._read_file('file1'))
        self.assertEqual(set(['file1', 'file1.tpl']),
                         set(os.listdir(self._tmp_dir)))

    def _write_file(self, filename, content):
        abs_filename = os.path.join(self._tmp_dir, filename)
        with open(abs_filename, 'w') as fobj:
            fobj.write(content)

    def _read_file(self, filename):
        abs_filename = os.path.join(self._tmp_dir, filename)
        with open(abs_filename) as fobj:
            return fobj.read()

    def _new_tpl_processor(self, context):
        return _TemplatesProcessor(self._tmp_dir, context)

    def test_generate_doesnt_touch_not_tpl_files(self):
        self._write_file('file1', 'foobar\n')

        tpl_processor = self._new_tpl_processor({})
        tpl_processor.generate_files()

        self.assertEqual('foobar\n', self._read_file('file1'))
        self.assertEqual(['file1'], os.listdir(self._tmp_dir))
