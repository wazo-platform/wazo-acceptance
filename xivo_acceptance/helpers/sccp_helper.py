# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from contextlib import contextmanager
from lettuce import world


@contextmanager
def sccp_settings():
    settings = world.confd_client.sccp_general.get()
    yield settings
    world.confd_client.sccp_general.update(settings)


def disable_directmedia():
    with sccp_settings() as settings:
        settings['options']['directmedia'] = "no"


def enable_directmedia():
    with sccp_settings() as settings:
        settings['options']['directmedia'] = "yes"


def set_dialtimeout(timeout):
    with sccp_settings() as settings:
        settings['options']['dialtimeout'] = str(timeout)


def set_language(language):
    with sccp_settings() as settings:
        settings['options']['language'] = language
