# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from hamcrest import assert_that
from hamcrest import is_
from lettuce import step, world

from xivo_acceptance.helpers import directory_helper
from xivo_acceptance.lettuce import sysutils


@step(u'I restart "([^"]*)"$')
def i_restart_service(step, service_name):
    sysutils.restart_service(service_name)


@step(u'I restart wazo-dird$')
def i_restart_wazo_dird(step):
    directory_helper.restart_dird()


@step(u'Then the service "([^"]*)" is running')
def then_the_service_group1_is_running(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.is_process_running(pidfile)


@step(u'When I generate a core dump and remember the pid as "([^"]*)" and the epoch as "([^"]*)"')
def when_i_generate_a_core_dump_and_remember_the_pid_as_group1_and_the_epoch_as_group2(step, pid_var_name, epoch_var_name):
    res = sysutils.output_command(['ulimit -c 1024 && /usr/local/bin/core_dump'])
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


@step(u'Then the file "([^"]*)" does not exist')
def then_the_file_1_does_not_exist(step, file_name):
    assert_that(sysutils.path_exists(file_name), is_(False))


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
