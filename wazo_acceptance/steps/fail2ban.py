# Copyright 2016-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

import requests
from behave import given, then, when
from hamcrest import assert_that, has_item

_JAIL_OVERRIDE_FILE = '/etc/fail2ban/jail.d/zz-wazo-acceptance.local'

_FAIL2BAN_REGEX_ARGS = {
    'wazo-provd': {
        'log': '/var/log/wazo-provd-fail2ban.log',
        'regex': '/etc/fail2ban/filter.d/wazo-provd.conf',
    },
    'wazo-provd-key': {
        'log': '/var/log/wazo-provd-fail2ban.log',
        'regex': '/etc/fail2ban/filter.d/wazo-provd-key.conf',
    },
}


@then('fail2ban-regex for "{name}" matches {match_count} lines')
def then_fail2banregex_for_name_matches_x_lines(context, name, match_count):
    match_count = int(match_count)
    args = _FAIL2BAN_REGEX_ARGS[name]
    command = ['fail2ban-regex', args['log'], args['regex']]

    output = context.ssh_client.out_call(command)
    last_lines = output.splitlines()[-5:]

    expected = f'Lines: {match_count} lines, 0 ignored, {match_count} matched, 0 missed'
    assert_that(
        last_lines,
        has_item(expected),
        f'output did not match: command was {command}',
    )


@given('the fail2ban jails are overridden with:')
def given_the_fail2ban_jails_are_overridden_with(context):
    # A real ban blocks every port, SSH included: tests that trigger a ban must
    # use a short bantime so that the cleanup can reach the server again
    sections = []
    for row in context.table:
        options = row.as_dict()
        jail = options.pop('jail')
        lines = [f'[{jail}]'] + [f'{key} = {value}' for key, value in options.items()]
        sections.append('\n'.join(lines))
    context.remote_sysutils.write_content_file(_JAIL_OVERRIDE_FILE, '\n\n'.join(sections) + '\n')
    context.remote_sysutils.send_command(['fail2ban-client', 'reload'])

    def remove_override():
        context.remote_sysutils.send_command(['rm', '-f', _JAIL_OVERRIDE_FILE])
        context.remote_sysutils.send_command(['fail2ban-client', 'reload'])

    context.add_cleanup(remove_override)


@then('the provisioning server refuses my connections')
def then_the_provisioning_server_refuses_my_connections(context):
    # fail2ban polls its log files: the ban is not immediate
    for _ in range(30):
        if not _provisioning_server_is_reachable(context):
            return
        time.sleep(1)
    raise AssertionError('the provisioning server still accepts connections: IP not banned')


@when('I wait until the provisioning server accepts my connections')
def when_i_wait_until_the_provisioning_server_accepts_my_connections(context):
    for _ in range(120):
        if _provisioning_server_is_reachable(context):
            return
        time.sleep(1)
    raise AssertionError('the provisioning server still refuses connections: IP still banned')


@then('fail2ban banned an IP address in jail "{jail}"')
def then_fail2ban_banned_an_ip_address_in_jail(context, jail):
    output = context.ssh_client.out_call(['grep', '-F', f"'[{jail}] Ban '", '/var/log/fail2ban.log'])
    assert output.strip(), f'no ban found for jail {jail} in /var/log/fail2ban.log'


def _provisioning_server_is_reachable(context):
    host = context.wazo_config['provd']['provisioning_host']
    try:
        requests.get(f'https://{host}/device/provisioning/', verify=False, timeout=3)
    except requests.exceptions.RequestException:
        return False
    return True
