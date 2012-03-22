# -*- coding: UTF-8 -*-

import os.path
import screen
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


class ScenarioException(Exception):
    pass


class ScenarioRunner(object):
    _SESSION_PREFIX = 'loadtester-'
    _SESSION_PREFIX_LENGTH = len(_SESSION_PREFIX)

    def attach_to_first_scenario(self):
        scenario_names = self.list_running_scenarios()
        if not scenario_names:
            raise ScenarioException('no scenario currently running')
        else:
            self._attach_to_scenario_by_name(scenario_names[0])

    def _attach_to_scenario_by_name(self, scenario_name):
        session_name = self._scenario_name_to_session_name(scenario_name)
        process = subprocess.Popen(['screen', '-r', session_name, '-x'])
        process.communicate()

    def _scenario_name_to_session_name(self, scenario_name):
        return self._SESSION_PREFIX + scenario_name

    def _session_name_to_scenario_name(self, session_name):
        return session_name[self._SESSION_PREFIX_LENGTH:]

    def attach_to_scenario(self, scenario):
        if scenario.name not in self.list_running_scenarios():
            raise ScenarioException("scenario '%s' is not running" % scenario.name)
        else:
            self._attach_to_scenario_by_name(scenario.name)

    def start_scenario(self, scenario, scenario_config):
        if scenario.name in self.list_running_scenarios():
            raise ScenarioException("scenario '%s' is already started" % scenario.name)
        else:
            session_name = self._scenario_name_to_session_name(scenario.name)
            context = scenario_config.get_context_for_scenario(scenario.name)
            scenario.prepare_start(context)
            process = subprocess.Popen(['screen', '-S', session_name, '-c', 'screenrc'],
                                       cwd=scenario.directory)
            process.communicate()

    def list_running_scenarios(self):
        return [self._session_name_to_scenario_name(session_name) for
                session_name in screen.get_session_names() if
                session_name.startswith(self._SESSION_PREFIX)]
