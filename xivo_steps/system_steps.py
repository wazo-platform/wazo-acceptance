# -*- coding: utf-8 -*-
import re

from lettuce import step
from xivo_lettuce import sysutils, assets
from lettuce.registry import world


@step(u'When I generate a core dump and remember the pid as "([^"]*)" and the epoch as "([^"]*)"')
def when_i_generate_a_core_dump_and_remember_the_pid_as_group1_and_the_epoch_as_group2(step, pid_var_name, epoch_var_name):
    assets.copy_asset_to_server('core_dump', '/tmp')
    res = sysutils.output_command(['ulimit -c 1024 && /tmp/core_dump'])
    separator = ': '
    for line in res.split('\n'):
        if separator not in line:
            continue
        name, value = line.split(separator, 1)
        if name == 'PID':
            setattr(world, pid_var_name, value)
        elif name == 'Epoch time':
            setattr(world, epoch_var_name, value)


@step(u'Then there should be a file name "([^"]*)"')
def then_there_should_be_a_file_name_group1(step, filename_pattern):
    filename = _replace_variables(filename_pattern)

    path = '~/%s' % filename

    assert sysutils.path_exists(path)


def _replace_variables(raw_string):
    pattern = r'\${(\w+)}'
    mappings = _extract_variable(pattern, raw_string)
    resolve = lambda match: mappings.get(match.group(0)[2:-1])
    return re.sub(pattern, resolve, raw_string)


def _extract_variable(pattern, raw_string):
    variable_names = re.findall(pattern, raw_string)
    res = []
    for name in variable_names:
        value = getattr(world, name)
        res.append(value)
    return dict(zip(variable_names, res))
