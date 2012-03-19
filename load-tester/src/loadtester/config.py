# -*- coding: UTF-8 -*-


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
        return context

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
