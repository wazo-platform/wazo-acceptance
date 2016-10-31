# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique inc.
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

from lettuce import world
from StringIO import StringIO


def get_confgen_file(file_name):
    command = ['xivo-confgen', 'asterisk/%s' % file_name]
    return world.ssh_client_xivo.out_call(command).decode('utf-8')


def get_conf_option(filename, section, option_name):
    options = get_conf_options(filename, section, [option_name])
    for current_option_name, current_option_value in options:
        if current_option_name == option_name:
            return current_option_value
    return None


def get_conf_options(filename, section, option_names):
    """Return a list of (option_name, option_value) tuple."""
    command = ['xivo-confgen', 'asterisk/%s' % filename]
    output = world.ssh_client_xivo.out_call(command)
    fobj = StringIO(output.decode('utf-8'))

    conf_helper = _AsteriskConfHelper(section, option_names)
    conf_helper.parse(fobj)
    return conf_helper.result


class _AsteriskConfHelper(object):

    def __init__(self, section, option_names):
        self._section = section
        self._option_names = list(option_names)
        self.result = []

    def parse(self, fobj):
        fun = self._parse_not_in_section
        while fun:
            fun = fun(fobj)

    def _parse_not_in_section(self, fobj):
        match = u'[%s]' % self._section
        for line in fobj:
            if line.startswith(match):
                return self._parse_in_section
        return None

    def _parse_in_section(self, fobj):
        for line in fobj:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(u'['):
                # start of a new section
                break
            option_name, option_value = self._extract_option_value_of_line(line)
            if option_name not in self._option_names:
                continue
            self.result.append((option_name, option_value))
        # supose there's only one section, so return None
        return None

    def _extract_option_value_of_line(self, line):
        try:
            option_name, option_value = line.split(u'=>', 1)
        except ValueError:
            option_name, option_value = line.split(u'=', 1)
        option_name = option_name.rstrip()
        option_value = option_value.lstrip()
        return option_name, option_value


def send_to_asterisk_cli(asterisk_command):
    world.ssh_client_xivo.call(_format_command(asterisk_command))


def check_output_asterisk_cli(asterisk_command):
    output = world.ssh_client_xivo.out_call(_format_command(asterisk_command))
    return output.decode('utf-8')


def _format_command(asterisk_command):
    return ['asterisk', '-rx', '"{}"'.format(asterisk_command)]
