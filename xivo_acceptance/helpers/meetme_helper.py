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

from lettuce import world


def delete_all_meetmes():
    confrooms = world.ws.confrooms.list()
    for confroom in confrooms:
        world.ws.confrooms.delete(confroom.id)


def delete_meetme_with_confno(confno):
    for meetme in _search_meetmes_by_confno(confno):
        world.ws.confrooms.delete(meetme.id)


def _search_meetmes_by_confno(confno):
    return world.ws.confrooms.search_by_number(confno)
