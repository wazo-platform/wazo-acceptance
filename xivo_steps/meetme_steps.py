# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce.common import open_url, remove_all_elements
from xivo_lettuce.manager import meetme_manager
from xivo_lettuce.manager_ws import meetme_manager_ws
from xivo_lettuce.xivoclient import xivoclient

@step(u'Given there are no conference rooms')
def given_there_are_no_conference_rooms(step):
    meetme_manager_ws.delete_all_meetmes()


@step(u'When I add the following conference rooms:')
def when_i_add_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_manager.create_meetme(meetme)


@step(u'Then the following conference rooms appear in the conference room xlet:')
def then_the_following_conference_rooms_appear_in_the_list(step):
    for meetme in step.hashes:
        assert_conference_room_1_has_number_2_in_xlet(meetme['name'], meetme['number'])
        if 'pin code' in meetme:
            assert_conference_room_1_has_pin_code_2_in_xlet(meetme['name'], meetme['pin code'])

@xivoclient
def assert_conference_room_1_has_number_2_in_xlet(confname, confnumber):
    assert world.xc_response == "OK"

@xivoclient
def assert_conference_room_1_has_pin_code_2_in_xlet(confname, pincode):
    assert world.xc_response == "OK"

@step(u'When I update the following conference rooms:')
def when_i_update_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_manager.update_meetme(meetme)
