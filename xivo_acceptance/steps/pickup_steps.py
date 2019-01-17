# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.action.webi import pickup as pickup_action_webi
from xivo_acceptance.lettuce import common, form


@step(u'Given there are pickups:$')
def given_there_are_pickup(step):
    for data in step.hashes:
        _delete_pickup(data['name'])
        pickup_action_webi.add_pickup(data)


def _delete_pickup(name):
    common.open_url('pickup')
    _pickup_search(name)
    common.remove_element_if_exist('pickup', name)
    _pickup_search('')


def _pickup_search(term):
    form.input.set_text_field_with_id('it-toolbar-search', term)
    form.submit.submit_form('it-toolbar-subsearch')
