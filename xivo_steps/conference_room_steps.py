# -*- coding: utf-8 -*-
from lettuce import step
from xivo_lettuce.common import remove_all_elements
from xivo_lettuce import world

@step(u'Given there are no conference rooms')
def given_there_are_no_conference_rooms(step):
    remove_all_elements('conference_room')

@step(u'When I add the following conference rooms:')
def when_i_add_the_following_conference_rooms(step):
    assert False, 'This step must be implemented'

@step(u'When I go to the conference room xlet')
def when_i_go_to_the_conference_room_xlet(step):
    assert False, 'This step must be implemented'

@step(u'Then the following conference rooms appear in the list:')
def then_the_following_conference_rooms_appear_in_the_list(step):
    assert False, 'This step must be implemented'

