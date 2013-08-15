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

from lettuce import world
from xivo_dao.helpers import db_manager
from sqlalchemy.sql import text


def exec_sql_request(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    world.ssh_client_xivo.check_call(command)


def exec_sql_request_with_return(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    return world.ssh_client_xivo.out_call(command)


def execute_sql(query, **args):
    return db_manager._asterisk_engine.execute(text(query), args)
