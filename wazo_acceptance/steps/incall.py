# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there is an incall "{exten}@{exten_context}" to the user "{firstname} {lastname}"')
def given_there_is_an_incall_to_the_user(context, exten, exten_context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)

    body = {'destination': {'type': 'user', 'user_id': confd_user['id']}}
    incall = context.helpers.incall.create(body)

    body = {'exten': exten, 'context': exten_context}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the IVR "{ivr_name}"')
def given_there_is_an_incall_to_the_ivr(context, exten, exten_context, ivr_name):
    ivr = context.helpers.ivr.get_by(name=ivr_name)

    body = {'destination': {'type': 'ivr', 'ivr_id': ivr['id']}}
    incall = context.helpers.incall.create(body)

    body = {'exten': exten, 'context': exten_context}
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

    body = {'exten': exten, 'context': exten_context}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)


@given('there is an incall "{exten}@{exten_context}" to the queue "{queue_name}"')
def given_there_is_an_incall_to_the_queue(context, exten, exten_context, queue_name):
    queue = context.helpers.queue.get_by(name=queue_name)

    body = {'destination': {'type': 'queue', 'queue_id': queue['id']}}
    incall = context.helpers.incall.create(body)

    body = {'exten': exten, 'context': exten_context}
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

    body = {'exten': exten, 'context': exten_context}
    extension = context.helpers.extension.create(body)

    context.helpers.incall.add_extension(incall, extension)
