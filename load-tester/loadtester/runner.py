# -*- coding: UTF-8 -*-

import subprocess


class ScenarioRunner(object):

    def start_scenario(self, scenario, scenario_config):
        context = scenario_config.get_context_for_scenario(scenario.name)
        scenario.prepare_start(context)
        process = subprocess.Popen(['sh', 'start.sh'], cwd=scenario.directory)
        process.communicate()
