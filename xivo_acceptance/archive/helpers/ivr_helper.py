# -*- coding: utf-8 -*-
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def add_or_replace_ivr(ivr):
    delete_ivr_with_name(ivr['name'])
    add_ivr(ivr)


def add_ivr(ivr):
    world.confd_client.ivr.create(ivr)


def delete_ivr_with_name(ivr_name):
    for ivr in world.confd_client.ivr.list(name=ivr_name)['items']:
        world.confd_client.ivr.delete(ivr['id'])
