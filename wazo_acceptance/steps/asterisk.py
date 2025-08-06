# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import assert_that, equal_to, has_entries, has_item, not_
from wazo_test_helpers import until

FUNCKEYS_EXTEN = {
    'unconditional': 21,
    'noanswer': 22,
    'busy': 23,
    'enablednd': 25,
    'incallfilter': 27,
    'bsfilter': 37,
}


@then('I have the following hints:')
def then_i_have_the_following_hints(context):
    output = context.helpers.asterisk.send_to_asterisk_cli('core show hints').split('\n')
    output = output[2:-3]  # strip header and footer
    hints = [{'exten': line[:30].strip(), 'line': line[32:94].strip()} for line in output]

    for row in context.table:
        row = row.as_dict()
        exten, exten_context = row['exten'].split('@')
        exten_context = context.helpers.context.get_by(label=exten_context)['name'][:25]
        row['exten'] = f'{exten}@{exten_context}'
        assert_that(hints, has_item(has_entries(row)))


@then('"{firstname} {lastname}" has function key "{position}" hint enabled')
def then_the_user_has_funckey_hint_enabled(context, firstname, lastname, position):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckey = context.confd_client.users(confd_user).get_funckey(int(position))
    prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
    until.true(_assert_inuse_hints_state, context, prefix_exten, tries=10)


@then('"{firstname} {lastname}" has function key "{position}" hint disabled')
def then_the_user_has_funckey_hint_disabled(context, firstname, lastname, position):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckey = context.confd_client.users(confd_user).get_funckey(int(position))
    prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
    until.true(_assert_idle_hints_state, context, prefix_exten, tries=10)


def _get_funckey_prefix_exten(user_id, funckey):
    if funckey['destination']['type'] == 'forward':
        funckey_exten = FUNCKEYS_EXTEN[funckey['destination']['forward']]
        if funckey['destination']['exten']:
            funckey_exten = '{}*{}'.format(funckey_exten, funckey['destination']['exten'])
    elif funckey['destination']['type'] == 'service':
        funckey_exten = FUNCKEYS_EXTEN[funckey['destination']['service']]
    elif funckey['destination']['type'] == 'bsfilter':
        funckey_exten = FUNCKEYS_EXTEN[funckey['destination']['type']]
        member_id = funckey['destination']['filter_member_id']
        return f'*{funckey_exten}{member_id}'
    else:
        raise Exception('Function key exten not found')

    return f'*735{user_id}***2{funckey_exten}'


def _assert_inuse_hints_state(context, prefix_exten):
    state = _get_hints_state(context, prefix_exten)
    if state != 'InUse':
        return False
    return True


def _assert_idle_hints_state(context, prefix_exten):
    state = _get_hints_state(context, prefix_exten)
    if state != 'Idle':
        return False
    return True


def _get_hints_state(context, prefix_exten):
    default_context = context.helpers.context.get_by(label='default')['name']
    hint = context.amid_client.action(
        'ExtensionState', {'Exten': prefix_exten, 'Context': default_context}
    )[0]
    assert_that(hint['Status'], not_(equal_to('-1')), f"Hint {prefix_exten} doesn't exist")
    return hint['StatusText']


@then('"{firstname} {lastname}" has all forwards hints enabled')
def then_the_user_has_all_forwards_hints_enabled(context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckeys = context.confd_client.users(confd_user).list_funckeys()['keys']
    for funckey in funckeys.values():
        prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
        until.true(_assert_inuse_hints_state, context, prefix_exten, tries=10)


@then('"{firstname} {lastname}" has all forwards hints disabled')
def then_the_user_has_all_forwards_hints_disabled(context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckeys = context.confd_client.users(confd_user).list_funckeys()['keys']
    for funckey in funckeys.values():
        prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
        until.true(_assert_idle_hints_state, context, prefix_exten, tries=10)
