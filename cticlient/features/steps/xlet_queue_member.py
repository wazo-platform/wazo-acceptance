# -*- coding: UTF-8 -*-

from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step


@step(u'Then the Queue members xlet is empty')
@xivoclient_step
def then_the_queue_members_xlet_is_empty(step):
    assert world.xc_response == 'OK'
