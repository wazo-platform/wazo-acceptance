# -*- coding: utf-8 -*-
# Copyright 2014-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from lettuce.registry import world

_DESCRIPTION_TO_FEATURE = {
    'Enable forwarding on no-answer': 'fwdrna',
    'Enable forwarding on busy': 'fwdbusy',
    'Enable unconditional forwarding': 'fwdunc',
    'Do not disturb': 'enablednd',
    'Incoming call filtering': 'incallfilter',
    'Call recording': 'callrecord',
}


@step(u'Given the "([^"]*)" extension is (disabled|enabled)')
def given_the_extension_is_disabled(step, description, state):
    feature = _DESCRIPTION_TO_FEATURE[description]
    extension = world.confd_client.extensions_features.list(feature=feature)['items'][0]
    extension['enabled'] = True if state == 'enabled' else False
    world.confd_client.extensions_features.update(extension)


@step(u'Given the "([^"]*)" extension is set to "([^"]*)"')
def given_the_extension_is_set_to(step, description, exten):
    feature = _DESCRIPTION_TO_FEATURE[description]
    extension = world.confd_client.extensions_features.list(feature=feature)['items'][0]
    extension['exten'] = _convert_to_pattern_if_needed(exten)
    world.confd_client.extensions_features.update(extension)


def _convert_to_pattern_if_needed(exten):
    if exten.endswith('.'):
        return '_{}'.format(exten)
    return exten
