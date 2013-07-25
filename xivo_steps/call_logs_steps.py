# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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


from lettuce import step, world
from xivo_lettuce import common
from xivo_lettuce import form, assets
from xivo_lettuce.manager import call_logs_manager


@step(u'When I request call_logs for today')
def when_i_request_call_logs_for_today(step):
    common.open_url('cel')
    form.submit.submit_form()


@step(u'Given there are a lot of calls on the date "([^"]*)"')
def given_there_are_a_lot_of_calls_on_the_date_1(step, date):
    sql_file_name = 'cel-extract.sql'
    server_dir = '/tmp'
    assets.copy_asset_to_server(asset=sql_file_name, serverpath=server_dir)
    remote_path = '%s/%s' % (server_dir, sql_file_name)

    change_cel_date_command = ['sed', '-i', "s/DATE/%s/g" % date, remote_path]
    world.ssh_client_xivo.check_call(change_cel_date_command)

    cel_insertion_command = ['sudo', '-u', 'postgres', 'psql', 'asterisk', '-c', '"\i %s"' % remote_path]
    world.ssh_client_xivo.check_call(cel_insertion_command)


@step(u'When I request call_logs for "([^"]*)"')
def when_i_request_call_logs_for_1(step, date):
    common.open_url('cel')
    call_logs_manager.type_date(date)
    form.submit.submit_form()
