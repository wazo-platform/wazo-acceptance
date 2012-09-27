# -*- coding: utf-8 -*-
import json

from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient_step, xivoclient


@step(u'When I enable screen pop-up')
@xivoclient_step
def when_i_enable_screen_pop_up(step):
    assert world.xc_response == 'OK'


@step(u'Then I see a sheet with the following values:')
def then_i_see_a_sheet_with_the_following_values(step):
    @xivoclient
    def then_i_see_a_sheet_with_variables_and_values(variable_map):
        pass
    then_i_see_a_sheet_with_variables_and_values(json.dumps(step.hashes))
    assert world.xc_response == 'OK'
