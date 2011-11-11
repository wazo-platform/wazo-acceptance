# -*- coding: UTF-8 -*-

import os
import subprocess
from loadtester import screen

SESSION_PREFIX = "loadtester-"


class ScenarioException(Exception):
    pass


def _extract_scenario_name(scenario_dir):
    return os.path.basename(scenario_dir.rstrip("/"))


def _get_session_name(scenario_name):
    return SESSION_PREFIX + scenario_name


def attach_to_scenario(scenario_dir):
    scenario_name = _extract_scenario_name(scenario_dir)
    if scenario_name not in list_running_scenarios():
        raise ScenarioException("scenario '%s' is not running" % scenario_name)
    else:
        session_name = _get_session_name(scenario_name)
        process = subprocess.Popen(["screen", "-r", session_name, "-x"])
        process.communicate()


def start_scenario(scenario_dir):
    scenario_name = _extract_scenario_name(scenario_dir)
    if scenario_name in list_running_scenarios():
        raise ScenarioException("scenario '%s' is already started" % scenario_name)
    else:
        old_cwd = os.getcwd()
        os.chdir(scenario_dir)
        try:
            session_name = _get_session_name(scenario_name)
            process = subprocess.Popen(["screen", "-S", session_name, "-c", "screenrc"])
            process.communicate()
        finally:
            os.chdir(old_cwd)


def list_running_scenarios():
    return [session[len(SESSION_PREFIX):] for
            session in screen.get_sessions() if
            session.startswith(SESSION_PREFIX)]
