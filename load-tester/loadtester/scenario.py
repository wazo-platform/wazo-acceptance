# -*- coding: UTF-8 -*-

import os.path
import subprocess
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class Scenario(object):
    def __init__(self, directory):
        self.directory = directory
        self.name = self._extract_scenario_name()

    def _extract_scenario_name(self):
        return os.path.basename(self.directory.rstrip("/"))

    def prepare_start(self, context):
        tpl_processor = _TemplatesProcessor(self.directory, context)
        tpl_processor.generate_files()


class _TemplatesProcessor(object):
    _TEMPLATE_SUFFIX = '.tpl'
    _TEMPLATE_SUFFIX_LENGTH = len(_TEMPLATE_SUFFIX)

    def __init__(self, directory, context):
        self._directory = directory
        self._context = context
        self._environment = Environment(loader=FileSystemLoader(directory),
                                        undefined=StrictUndefined)

    def generate_files(self):
        for tpl_filename in self._list_template_filenames():
            self._generate_file_from_template(tpl_filename)

    def _list_template_filenames(self):
        for filename in os.listdir(self._directory):
            if self._is_template_filename(filename):
                yield filename

    def _is_template_filename(self, filename):
        return filename.endswith(self._TEMPLATE_SUFFIX)

    def _generate_file_from_template(self, tpl_filename):
        filename = self._get_template_destination(tpl_filename)
        template = self._environment.get_template(tpl_filename)
        template.stream(self._context).dump(filename)

    def _get_template_destination(self, tpl_filename):
        filename = tpl_filename[:-self._TEMPLATE_SUFFIX_LENGTH]
        return os.path.join(self._directory, filename)


class ScenarioRunner(object):

    def start_scenario(self, scenario, scenario_config):
        context = scenario_config.get_context_for_scenario(scenario.name)
        scenario.prepare_start(context)
        process = subprocess.Popen(['sh', 'start.sh'], cwd=scenario.directory)
        process.communicate()
