# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import re

from lettuce import step
from lettuce.registry import world

from xivo_acceptance.lettuce import sysutils, assets


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

    assert sysutils.path_exists(path), 'No such file or directory %s' % path


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
