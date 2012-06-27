# -*- coding: UTF-8 -*-

import logging
import time

logger = logging.getLogger(__name__)


class ScenarioConfig(object):
    def __init__(self, config_content):
        self._config = {}
        self._scenarios = _ScenariosObject()
        self._read_config(config_content)

    def _read_config(self, config_content):
        self._config['scenarios'] = self._scenarios
        exec config_content in self._config
        del self._config['scenarios']
        del self._config['__builtins__']

    def get_context_for_scenario(self, scenario_name):
        context = dict(self._config)
        attribute_name = scenario_name.replace('-', '_')
        scenario_object = getattr(self._scenarios, attribute_name)
        context.update(scenario_object.__dict__)
        context['sipp_std_options'] = self._compute_sipp_std_options(context)
        self._emit_deprecation_warning(context)
        return context

    _SIPP_STD_OPTIONS = [
        ('sipp_local_ip', '-i'),
        ('sipp_call_rate', '-r'),
        ('sipp_pause_in_ms', '-d'),
        ('sipp_rate_period_in_ms', '-rp'),
        ('sipp_max_simult_calls', '-l'),
    ]

    _SIPP_STD_FLAGS = [
        ('sipp_enable_trace_stat', '-trace_stat')
    ]

    def _compute_sipp_std_options(self, context):
        sipp_std_options_list = []
        for key, option_flag in self._SIPP_STD_OPTIONS:
            if key in context:
                sipp_std_options_list.extend([option_flag, str(context[key])])
        for key, option_flag in self._SIPP_STD_FLAGS:
            if context.get(key, False):
                sipp_std_options_list.extend([option_flag])
        return ' '.join(sipp_std_options_list)

    def _emit_deprecation_warning(self, context):
        if 'sipp_pause_in_ms' in context:
            logger.warning('deprecated config key "sipp_pause_in_ms": please use "pause"')
            time.sleep(3)

    @classmethod
    def new_from_filename(cls, filename):
        with open(filename) as fobj:
            config_content = fobj.read()
        return cls(config_content)


class _ScenariosObject(object):
    def __init__(self):
        self._scenarios = {}

    def __getattr__(self, name):
        return self._scenarios.setdefault(name, _ScenarioObject())


class _ScenarioObject(object):
    pass
