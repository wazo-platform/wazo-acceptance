# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world
from hamcrest import assert_that, is_not, none
from requests.exceptions import HTTPError

from xivo_auth_client import Client as AuthClient
from xivo_acceptance import helpers
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.helpers import (
    cti_profile_helper,
    entity_helper,
    group_helper,
    line_read_helper,
    line_write_helper,
    sip_config,
    sip_phone,
    tenant_helper,
    voicemail_helper,
)
from xivo_acceptance.lettuce import postgres


def add_or_replace_user(userinfo):
    delete_similar_users(userinfo)
    tenant_uuid = tenant_helper.get_tenant_uuid()
    userinfo['tenant_uuid'] = tenant_uuid
    user = world.confd_client.users.create(userinfo)
    auth_user = {
        'uuid': user['uuid'],
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'username': userinfo.get('username', userinfo.get('email', user['uuid'])),
        'password': userinfo.get('password') or None,
        'email_address': user['email'],
        'enabled': True,
        'tenant_uuid': tenant_uuid,
    }
    world.auth_client.users.new(**auth_user)


def find_by_user_id(user_id):
    try:
        return world.confd_client.users.get(user_id)
    except HTTPError:
        return None


def get_by_exten_context(exten, context):
    user = find_by_exten_context(exten, context)
    assert_that(user, is_not(none()),
                "User with exten %s@%s not found" % (exten, context))
    return user


def find_by_exten_context(exten, context):
    response = world.confd_client.users.list(exten=exten, context=context, recurse=True, view='summary')
    for user in response['items']:
        return user


def find_by_firstname_lastname(firstname, lastname=None):
    kwargs = {
        'firstname': firstname,
        'recurse': True,
    }
    if lastname:
        kwargs['lastname'] = lastname

    response = world.confd_client.users.list(**kwargs)
    for user in response['items']:
        # The user was searched by firstname & lastname the result matches
        if lastname:
            return user

        # We searched without a lastname confd returned results for every user with the matching
        # firstname and ignored the lastname argument
        if not user['lastname']:
            return user


def get_by_firstname_lastname(firstname, lastname=None):
    user = find_by_firstname_lastname(firstname, lastname)
    assert_that(
        user,
        is_not(none()),
        u"user '{}' does not exist".format(u'{} {}'.format(firstname, lastname).strip()).encode('utf8')
    )
    return user


def get_user_by_name(name):
    names = name.split(" ", 1)
    return get_by_firstname_lastname(*names)


def delete_similar_users(userinfo):
    if 'firstname' in userinfo and 'lastname' in userinfo:
        user = find_by_firstname_lastname(userinfo['firstname'],
                                          userinfo['lastname'])
        if user:
            delete_user(user['id'])


def delete_user(user_id):
    user = world.confd_client.users.get(user_id)
    _delete_voicemail(user)
    _delete_line_associations(user)
    _delete_user(user)


def _delete_line_associations(user):
    for line in user['lines']:
        line = world.confd_client.lines.get(line['id'])
        line_write_helper.dissociate_device(line)
        line_write_helper.dissociate_users(line)


def _delete_voicemail(user):
    voicemail_id = voicemail_helper.find_voicemail_by_user_id(user['id'])
    if voicemail_id:
        voicemail_helper.delete_voicemail(voicemail_id)


def _delete_user(user):
    world.confd_client.users.delete(user['id'])
    world.auth_client.users.delete(user['uuid'])


def add_user_with_infos(user_data, step=None):
    user = dict(user_data)
    user.setdefault('entity_name', world.config['default_entity'])

    if user.get('number') and user.get('context'):
        user['line_number'] = user.pop('number')
        user['line_context'] = user.pop('context')

    if 'voicemail_name' in user:
        user.setdefault('language', 'en_US')

    if user.get('cti_profile'):
        user['enable_client'] = True
        user['client_profile'] = user.pop('cti_profile')

    user['client_username'] = user.pop('cti_login', user['firstname'].lower())
    user['client_password'] = user.pop('cti_passwd', user['lastname'].lower())

    user = {key: value for key, value in user.iteritems() if value is not None}
    user_id = helpers.user_line_extension_helper.add_or_replace_user(user, step=step)

    fullname = '{firstname} {lastname}'.format(**user).strip()
    if user.get('token', 'no') == 'yes':
        auth_client = AuthClient(
            world.config['xivo_host'],
            username=user['client_username'],
            password=user['client_password'],
            verify_certificate=False,
        )
        token_data = auth_client.token.new(backend='wazo_user', expiration=120)
        step.scenario.user_tokens[fullname] = token_data['token']

    if user.get('schedule'):
        user_action_webi.add_schedule(fullname, user['schedule'])

    if user.get('agent_number'):
        helpers.agent_helper.delete_agents_with_number(user['agent_number'])
        agent_data = {'firstname': user['firstname'],
                      'lastname': user['lastname'],
                      'number': user['agent_number'],
                      'users': [user_id]}
        helpers.agent_helper.add_agent(agent_data)

    if user.get('group_name'):
        user_created = world.confd_client.users.get(user_id)
        group_helper.add_or_replace_group(user['group_name'], users=[user_created])


def add_user(data_dict, step=None):
    tenant_uuid = None
    if 'entity_name' in data_dict:
        entity = entity_helper.get_entity_with_name(data_dict['entity_name'])
        if entity:
            tenant_uuid = entity['tenant']['uuid']
    else:
        tenant_uuid = tenant_helper.get_tenant_uuid()

    world.confd_client.set_tenant(tenant_uuid)
    world.auth_client.set_tenant(tenant_uuid)
    user = {}

    user['firstname'] = data_dict['firstname']

    if 'lastname' in data_dict:
        user['lastname'] = data_dict['lastname']
    if 'language' in data_dict:
        user['language'] = data_dict['language']
    if 'mobile_number' in data_dict:
        user['mobile_phone_number'] = data_dict['mobile_number'] or None

    user = world.confd_client.users.create(user)

    auth_user = {
        'uuid': user['uuid'],
        'username': data_dict.get('client_username', user['uuid']),
        'password': data_dict.get('client_password'),
        'enabled': data_dict.get('enable_client', True),
    }
    world.auth_client.users.new(**auth_user)

    if 'client_profile' in data_dict:
        profile_id = cti_profile_helper.find_profile_id_by_name(data_dict['client_profile'])
        world.confd_client.users(user['uuid']).update_cti_profile(
            {'id': profile_id},
            enabled=False,  # enabled is handled by wazo-auth
        )

    if 'agentid' in data_dict:
        world.confd_client.users(user['uuid']).add_agent(data_dict['agentid'])

    if 'line_number' in data_dict and 'line_context' in data_dict:
        extension_data = {'context': data_dict['line_context'],
                          'exten': data_dict['line_number']}
        extension = world.confd_client.extensions.create(extension_data)
        line_data = {
            'context': data_dict['line_context'],
        }
        if 'device_slot' in data_dict:
            line_data['position'] = data_dict['device_slot']
        if 'max_contacts' in data_dict:
            line_data['max_contacts'] = data_dict['max_contacts']
        line = world.confd_client.lines.create(line_data)

        protocol = data_dict.get('protocol', 'sip')
        if protocol == 'sip':
            endpoint = world.confd_client.endpoints_sip.create({})
            world.confd_client.lines(line['id']).add_endpoint_sip(endpoint)
        elif protocol == 'sccp':
            endpoint = world.confd_client.endpoints_sccp.create({})
            world.confd_client.lines(line['id']).add_endpoint_sccp(endpoint)
        elif protocol == 'custom':
            endpoint = world.confd_client.endpoints_custom.create({})
            world.confd_client.lines(line['id']).add_endpoint_custom(endpoint)

        world.confd_client.lines(line['id']).add_extension(extension)
        world.confd_client.users(user['uuid']).add_line(line['id'])

        mac = data_dict.get('device')
        if mac:
            device = world.confd_client.devices.list(mac=mac)['items'][0]
            world.confd_client.lines(line['id']).add_device(device['id'])

    if {'voicemail_name', 'voicemail_number', 'voicemail_context'}.issubset(data_dict):
        voicemail = voicemail_helper.add_or_replace_voicemail({
            'name': data_dict['voicemail_name'],
            'number': data_dict['voicemail_number'],
            'context': data_dict['voicemail_context'],
        })
        world.confd_client.users.relations(user['uuid']).add_voicemail(voicemail)

    if data_dict.get('with_phone', 'yes') == 'yes' and step:
        _register_and_track_phone(step.scenario, data_dict)

    return user['id']


def _register_and_track_phone(scenario, user_data):
    phone_available = user_data.get('protocol') == 'sip' and 'line_number' in user_data
    if not phone_available:
        return

    number = user_data['line_number']
    context = user_data.get('line_context', 'default')
    line = line_read_helper.find_with_exten_context(number, context)
    if not line or not line['endpoint_sip']:
        return

    name = ('%s %s' % (user_data.get('firstname', ''),
                       user_data.get('lastname', ''))).strip()

    endpoint_sip = world.confd_client.endpoints_sip.get(line['endpoint_sip']['id'])
    max_contacts = int(user_data.get('max_contacts') or 1)
    for _ in xrange(max_contacts):
        phone_config = sip_config.create_config(world.config, scenario.phone_register, endpoint_sip)
        phone = sip_phone.register_line(phone_config)
        phone.sip_contact_uri = scenario.phone_register.find_new_sip_contact(line['name'])
        if phone:
            scenario.phone_register.add_registered_phone(phone, name)


def user_is_in_group(user, group):
    for group_user in group['members']['users']:
        if user['uuid'] == group_user['uuid']:
            return True
    return False


def disable_cti_client(firstname, lastname):
    users = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items']
    for user in users:
        auth_user = world.auth_client.users.get(user['uuid'])
        auth_user['enabled'] = False
        world.auth_client.users.edit(auth_user['uuid'], **auth_user)


def enable_cti_client(firstname, lastname):
    users = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items']
    for user in users:
        auth_user = world.auth_client.users.get(user['uuid'])
        auth_user['enabled'] = True
        world.auth_client.users.edit(auth_user['uuid'], **auth_user)


def get_unconditional_forward(fullname):
    firstname, lastname = fullname.split(' ', 1)
    query = """
    SELECT
        enableunc,
        destunc
    FROM
        userfeatures
    WHERE
        firstname = :firstname
        AND lastname = :lastname
    """

    rows = postgres.exec_sql_request(query, firstname=firstname, lastname=lastname).fetchall()
    if len(rows) != 1:
        raise Exception('expected 1 user "{} {}": got {}'.format(firstname, lastname, len(rows)))

    enabled, dest = rows[0]
    return bool(enabled), dest
