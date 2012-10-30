# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.manager import device_manager


@step(u'^Given there is a device with infos:$')
def given_there_is_a_device_with_infos(step):
    for info in step.hashes:
        device_manager.add_or_replace_device(info)


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, str):
    device_manager.search_device(str)
