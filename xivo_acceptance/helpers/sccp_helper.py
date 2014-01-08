# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from contextlib import contextmanager
from lettuce import world


@contextmanager
def sccp_settings():
    settings = world.ws.sccp_general_settings.view()
    yield settings
    dict_obj = settings.to_obj_dict()
    world.ws.sccp_general_settings.raw_edit(None, dict_obj)


def disable_directmedia():
    with sccp_settings() as settings:
        settings.directmedia = False


def enable_directmedia():
    with sccp_settings() as settings:
        settings.directmedia = True


def set_dialtimeout(timeout):
    with sccp_settings() as settings:
        settings.dialtimeout = timeout


def set_language(language):
    with sccp_settings() as settings:
        settings.language = language
