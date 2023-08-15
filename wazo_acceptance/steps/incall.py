# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there is an incall "{exten}@{exten_context}" to the user "{firstname} {lastname}"')
def given_there_is_an_incall_to_the_user(context, exten, exten_context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)

    body = {'destination': {'type': 'user', 'user_id': confd_user['id']}}
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the IVR "{ivr_name}"')
def given_there_is_an_incall_to_the_ivr(context, exten, exten_context, ivr_name):
    ivr = context.helpers.ivr.get_by(name=ivr_name)

    body = {'destination': {'type': 'ivr', 'ivr_id': ivr['id']}}
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the queue "{queue_name}" with skill "{skill_name}"')
def given_there_is_an_incall_to_the_queue_with_skill(context, exten, exten_context, queue_name, skill_name):
    queue = context.helpers.queue.get_by(name=queue_name)
    skill_rule = context.helpers.queue_skill_rule.get_by(name=skill_name)

    body = {
        'destination': {
            'type': 'queue',
            'queue_id': queue['id'],
            'skill_rule_id': skill_rule['id'],
        }
    }
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the queue "{queue_name}"')
def given_there_is_an_incall_to_the_queue(context, exten, exten_context, queue_name):
    queue = context.helpers.queue.get_by(name=queue_name)

    body = {'destination': {'type': 'queue', 'queue_id': queue['id']}}
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the group "{group_name}"')
def given_there_is_an_incall_to_the_group(context, exten, exten_context, group_name):
    group = context.helpers.confd_group.get_by(label=group_name)

    body = {'destination': {'type': 'group', 'group_id': group['id']}}
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the application "{app_name}"')
def given_there_is_an_incall_to_the_application(context, exten, exten_context, app_name):
    application = context.helpers.application.get_by(name=app_name)

    body = {
        'destination': {
            'type': 'application',
            'application': 'custom',
            'application_uuid': application['uuid']
        }
    }
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the switchboard "{name}"')
def given_there_is_an_incall_to_the_switchboard(context, exten, exten_context, name):
    switchboard = context.helpers.switchboard.get_by(name=name)

    body = {
        'destination': {
            'type': 'switchboard',
            'switchboard_uuid': switchboard['uuid']
        }
    }
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to DISA redirected to "{disa_context}" with pin "{pin}"')
def given_there_is_an_incall_to_DISA_with_context_and_pin(context, exten, exten_context, disa_context, pin):
    disa_context_name = context.helpers.context.get_by(label=disa_context)['name']
    body = {
        'destination': {
            'type': 'application',
            'application': 'disa',
            'context': disa_context_name,
            'pin': pin,
        }
    }
    incall = context.helpers.incall.create(body)

    context_name = context.helpers.context.get_by(label=exten_context)['name']
    body = {'exten': exten, 'context': context_name}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)
