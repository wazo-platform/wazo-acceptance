# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import ends_with
from hamcrest import has_entries
from lettuce import step, world
from xivo_acceptance.helpers import call_logs_helper, cel_helper
from xivo_acceptance.helpers.datetime_helper import close_to
from xivo_acceptance.lettuce import assets, common, sysutils


@step(u'Given there are no call logs$')
def given_there_are_no_call_logs(step):
    call_logs_helper.delete_all()


@step(u'Given I have only the following CEL entries:')
def given_i_have_only_the_following_cel_entries(step):
    cel_helper.delete_all()
    cel_helper.insert_entries(step.hashes)


@step(u'Given there are a lot of unprocessed calls')
def given_there_are_a_lot_of_calls(step):
    sql_file_name = 'cel-extract.sql'
    server_dir = '/tmp'
    assets.copy_asset_to_server(asset=sql_file_name, serverpath=server_dir)
    remote_path = '%s/%s' % (server_dir, sql_file_name)

    cel_insertion_command = ['sudo', '-u', 'postgres', 'psql', 'asterisk', '-f', remote_path]
    world.ssh_client_xivo.check_call(cel_insertion_command)


@step(u'Given there are only the following call logs:')
def given_there_are_only_the_following_call_logs(step):
    call_logs_helper.delete_all()
    call_logs_helper.create_call_logs(step.hashes)


@step(u'When I generate call logs$')
def when_i_generate_call_logs(step):
    command = ['wazo-call-logs']
    sysutils.send_command(command)


@step(u'When I generate call logs using the last (\d+) unprocessed CEL entries$')
def when_i_generate_call_logs_using_the_last_unprocessed_1_cel_entries(step, cel_count):
    command = ['wazo-call-logs', '-c', cel_count]
    sysutils.send_command(command)


@step(u'When I generate call logs twice in parallel')
def when_i_generate_call_logs_twice_in_parallel(step):
    command = ['wazo-call-logs', '&', 'wazo-call-logs']
    world.command_output = world.ssh_client_xivo.out_err_call(command)


@step(u'Then I see that call log generation is already running')
def then_i_see_that_call_log_generation_is_already_running(step):
    assert_that(world.command_output.rstrip(), ends_with('An other instance of ourself is probably running.'))


@step(u'Then I should have the following call logs:')
def then_i_should_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert call_logs_helper.has_call_log(entry), "Corresponding call_log entry was not found : %s" % entry


@step(u'Then I have the last call log matching:')
def then_i_have_the_last_call_log_matching(step):
    expected = dict(step.hashes[0])
    expected_duration = int(expected.pop('duration', None))
    if expected.get('answered'):
        expected['answered'] = bool(expected['answered'])

    def _assert():
        actual = world.call_logd_client.cdr.list(direction='desc', limit=1)['items'][0]
        assert_that(actual, has_entries(expected))
        if expected_duration:
            assert_that(actual['duration'], close_to(expected_duration, 2))

    common.wait_until_assert(_assert, tries=5)


@step(u'Then I should not have the following call logs:')
def then_i_should_not_have_the_following_call_logs(step):
    for entry in step.hashes:
        assert not call_logs_helper.has_call_log(entry), "Corresponding call_log entry was found : %s" % entry
