# -*- coding: utf-8 -*-

import os
import time
from lettuce import step, world
from hamcrest import assert_that, greater_than
from xivo_lettuce.common import open_url, find_line


@step(u'Given there is a backup file "([^"]*)"')
def given_there_is_a_backup_file(step, filename):
    command = 'dd if=/dev/zero of=/var/backups/xivo/%s bs=1024 count=200240' % filename
    world.ssh_client_xivo.out_call([command])


@step(u'When I download backup file "([^"]*)"')
def when_i_download_backup_file(step, filename):
    open_url('backups')
    table_line = find_line(filename)
    download_link = table_line.find_element_by_xpath(".//a[@title='%s']" % filename)
    download_link.click()


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
