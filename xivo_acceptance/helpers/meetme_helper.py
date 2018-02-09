# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world


def delete_meetme_with_confno(confno):
    for meetme in _search_meetmes_by_confno(confno):
        world.ws.confrooms.delete(meetme.id)


def _search_meetmes_by_confno(confno):
    return world.ws.confrooms.search_by_number(confno)
