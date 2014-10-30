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

import os
import time
from lettuce import step, world
from hamcrest import assert_that, greater_than
from xivo_acceptance.lettuce import assets, common


@step(u'Given there is a backup file "([^"]*)"')
def given_there_is_a_backup_file(step, filename):
    command = 'dd if=/dev/zero of=/var/backups/xivo/%s bs=1024 count=200240' % filename
    world.ssh_client_xivo.out_call([command])


@step(u'Given the asset file "([^"]*)" is copied on the server into "([^"]*)"')
def given_the_file_is_copied_on_the_server_into_group2(step, assetfile, serverpath):
    assets.copy_asset_to_server(assetfile, serverpath)


@step(u'When I download backup file "([^"]*)"')
def when_i_download_backup_file(step, filename):
    common.open_url('backups')
    table_line = common.get_line(filename)
    download_link = table_line.find_element_by_xpath(".//a[@title='%s']" % filename)
    download_link.click()


@step(u'When I execute database backup command')
def when_i_execute_database_backup_command(step):
    command = 'bash /tmp/xivo-backup-manager backup'
    world.ssh_client_xivo.out_call([command])


@step(u'When I execute database restore command')
def when_i_execute_database_restore_command(step):
    command = 'bash /tmp/xivo-backup-manager restore'
    world.ssh_client_xivo.out_call([command])


@step(u'Then a non-empty file "([^"]*)" is present on disk')
def then_a_non_empty_file_is_present_on_disk(step, filename):
    path = os.path.join('/', 'tmp', filename)
    filesize = 0
    for _ in range(30):
        time.sleep(1)
        is_file = os.path.isfile(path)
        if is_file:
            try:
                filesize = os.path.getsize(path)
                if filesize > 0:
                    break
            except OSError:
                raise Exception("Unknown file : %s" % path)

    assert_that(filesize, greater_than(0))
    os.remove(path)
