# -*- coding: UTF-8 -*-

from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step
from xivo_lettuce.manager_ws import queue_manager_ws


@step(u'Then the Queue members xlet is empty')
@xivoclient_step
def then_the_queue_members_xlet_is_empty(step):
    assert world.xc_response == 'OK'


@step(u'Then the Queue members xlet for queue "([^"]*)" is empty')
def then_the_queue_members_xlet_for_queue_1_is_empty(step, queue_name):
    queue_id = queue_manager_ws.get_queue_id_with_queue_name(queue_name)

    @xivoclient
    def then_the_queue_members_xlet_for_queue_1_is_empty_(queue_id):
        pass

    then_the_queue_members_xlet_for_queue_1_is_empty_(queue_id)
    assert world.xc_response == 'OK'


@step(u'When I enable the hide unlogged agents option')
@xivoclient_step
def when_i_enable_the_hide_unlogged_agents_option(step):
    assert world.xc_response == 'OK'


@step(u'Then the Queue members xlet for queue "([^"]*)" should display agents:')
def then_the_queue_members_xlet_for_queue_1_should_display_agents(step, queue_name):
    queue_id = queue_manager_ws.get_queue_id_with_queue_name(queue_name)

    @xivoclient
    def then_the_queue_members_xlet_for_queue_1_displays_agents(queue_id, variable_map):
        pass

    then_the_queue_members_xlet_for_queue_1_displays_agents(queue_id, step.hashes)
    assert world.xc_response == 'OK'
